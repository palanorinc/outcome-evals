"""Where series and questions come from.

- ``LocalData``: the files shipped in this package (or any directory laid out
  the same way). No key, no network.
- ``PalanorAPI``: Palanor's public API (``/v1/signals/<id>/observations``) with
  a key, so an organization can resolve its own calls against any series the
  API serves, not only the ones shipped here. A free key is at
  https://palanor.com/developers/keys. Every response carries the source's
  licence, which is kept on the series.

Layout of a data directory::

    series/series.json            metadata for each series (and "as_of")
    series/<id>.csv               id,timestamp,target
    questions/resolved_history.jsonl
    questions/live/<made_on>.jsonl
    resolutions.jsonl             {"id": ..., "resolution": {...}} for live questions
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable
from dataclasses import replace
from datetime import date
from importlib import resources
from pathlib import Path
from typing import Any

from ._meta import DIST, PALANOR_API
from ._version import __version__
from .calls import Call, Resolution, load_calls
from .series import Series, SeriesInfo, load_series_dir


def packaged_data_dir() -> Path:
    return Path(str(resources.files("outcome_evals") / "data"))


class LocalData:
    """Series and questions from a data directory (default: the files shipped with the package)."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else packaged_data_dir()
        self._series: dict[str, Series] | None = None

    @property
    def series_dir(self) -> Path:
        return self.root / "series"

    def manifest(self) -> dict[str, Any]:
        p = self.series_dir / "series.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"series": []}

    def all_series(self) -> dict[str, Series]:
        if self._series is None:
            self._series = load_series_dir(self.series_dir)
        return self._series

    def series(self, series_id: str) -> Series:
        s = self.all_series().get(series_id)
        if s is None:
            raise KeyError(f"no series {series_id!r} in {self.series_dir}")
        return s

    def resolutions(self) -> dict[str, Resolution]:
        p = self.root / "resolutions.jsonl"
        out: dict[str, Resolution] = {}
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    d = json.loads(line)
                    out[d["id"]] = Resolution.from_dict(d["resolution"])
        return out

    def live_files(self) -> list[Path]:
        return sorted((self.root / "questions" / "live").glob("*.jsonl"))

    def questions(self, split: str = "resolved_history") -> list[Call]:
        """``resolved_history``, ``live`` (every live batch, with any recorded resolutions), or ``all``."""
        if split == "all":
            return self.questions("resolved_history") + self.questions("live")
        if split == "resolved_history":
            p = self.root / "questions" / "resolved_history.jsonl"
            return load_calls(p) if p.exists() else []
        if split == "live":
            calls = load_calls(*self.live_files()) if self.live_files() else []
            res = self.resolutions()
            return [c.with_resolution(res.get(c.id, c.resolution)) for c in calls]
        raise ValueError(f"unknown split {split!r}: use resolved_history, live or all")


class PalanorAPIError(RuntimeError):
    pass


class PalanorAPI:
    """Read series from Palanor's public API. Needs a key (``PALANOR_API_KEY``)."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0, pause: float = 0.25) -> None:
        self.api_key = api_key or os.environ.get("PALANOR_API_KEY")
        if not self.api_key:
            raise PalanorAPIError("set PALANOR_API_KEY (a free key: https://palanor.com/developers/keys)")
        self.base_url = (base_url or os.environ.get("PALANOR_API_URL") or PALANOR_API).rstrip("/")
        self.timeout = timeout
        self.pause = pause
        self.requests = 0

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{self.base_url}{path}?{q}"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json", "User-Agent": f"{DIST}/{__version__}"},
        )
        delay = 2.0
        for attempt in range(5):
            try:
                self.requests += 1
                with urllib.request.urlopen(req, timeout=self.timeout) as r:  # noqa: S310 (fixed https base)
                    body: dict[str, Any] = json.loads(r.read().decode("utf-8"))
                    return body
            except urllib.error.HTTPError as e:
                text = e.read().decode("utf-8", "replace")[:300]
                if e.code in (429, 502, 503, 504) and attempt < 4 and "monthly" not in text.lower():
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise PalanorAPIError(f"GET {path}: HTTP {e.code}: {text}") from e
            except urllib.error.URLError as e:
                if attempt < 4:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise PalanorAPIError(f"GET {path}: {e.reason}") from e
        raise PalanorAPIError(f"GET {path}: gave up")

    def series(self, series_id: str, start: str | date | None = None, end: str | date | None = None, info: SeriesInfo | None = None) -> Series:
        """Every reading of a series in a window, following pages. Metadata comes from the response."""
        pairs: list[tuple[str, float]] = []
        offset = 0
        meta: dict[str, Any] = {}
        prov: dict[str, Any] = {}
        path = f"/signals/{urllib.parse.quote(series_id, safe='')}/observations"
        while True:
            body = self._get(path, {"start": str(start) if start else None, "end": str(end) if end else None, "limit": 1000, "offset": offset})
            data = body.get("data") or {}
            meta = data.get("signal") or meta
            prov = body.get("provenance") or prov
            for o in data.get("observations") or []:
                if o.get("value") is not None:
                    pairs.append((str(o["observed_at"])[:10], float(o["value"])))
            pg = body.get("pagination") or {}
            if not pg.get("has_more"):
                break
            offset = int(pg.get("next_offset") or offset + 1000)
            time.sleep(self.pause)
        base = info or SeriesInfo(id=series_id)
        inf = replace(
            base,
            name=base.name or str(meta.get("name") or ""),
            unit=base.unit or str(meta.get("unit") or ""),
            publisher=str(prov.get("publisher") or base.publisher),
            source=str(prov.get("source") or base.source),
            license=str(prov.get("license_name") or base.license),
            license_url=str(prov.get("license_url") or base.license_url),
            attribution=str(prov.get("attribution") or base.attribution),
            url=base.url or f"https://palanor.com/signals/{series_id}",
            extra={**base.extra, **({"license_class": prov["license_class"]} if prov.get("license_class") else {})},
        )
        return Series.from_pairs(inf, pairs, as_of=date.today())

    def many(self, series_ids: Iterable[str], start: str | date | None = None) -> dict[str, Series]:
        return {sid: self.series(sid, start=start) for sid in series_ids}


def series_for(calls: Iterable[Call], local: LocalData | None = None, api: PalanorAPI | None = None) -> dict[str, Series]:
    """The series a set of calls needs: from the API when given, else from local files."""
    ids = sorted({c.series_id for c in calls})
    if api is not None:
        return api.many(ids)
    loc = local or LocalData()
    have = loc.all_series()
    missing = [i for i in ids if i not in have]
    if missing:
        raise KeyError(f"series not in {loc.series_dir}: {', '.join(missing)}; pass a Palanor API key to fetch them")
    return {i: have[i] for i in ids}
