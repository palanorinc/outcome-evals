"""Dated series: what a call resolves against.

A series is a sorted list of ``(timestamp, value)`` readings plus what we know
about it: who publishes it, its licence, its cadence, how long after a period
the reading is published (``publish_lag_days``), and whether it has ended.

Files use the ``fev`` long format: a CSV with ``id``, ``timestamp`` and
``target`` columns, one row per reading.
"""

from __future__ import annotations

import bisect
import csv
import io
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SeriesInfo:
    """What is known about a series, apart from its readings."""

    id: str
    name: str = ""
    unit: str = ""
    period: str = "M"
    publish_lag_days: int = 0
    publisher: str = ""
    source: str = ""  # ledger slug of the data source, e.g. "bls"
    license: str = ""
    license_url: str = ""
    attribution: str = ""
    url: str = ""
    ended_on: date | None = None
    notes: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> SeriesInfo:
        known = {f for f in cls.__dataclass_fields__ if f != "extra"}
        kw: dict[str, Any] = {k: d[k] for k in known if k in d and k != "ended_on"}
        if d.get("ended_on"):
            kw["ended_on"] = date.fromisoformat(str(d["ended_on"]))
        if "publish_lag_days" in kw:
            kw["publish_lag_days"] = int(kw["publish_lag_days"])
        extra = {k: v for k, v in d.items() if k not in known}
        return cls(extra=extra, **kw)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "period": self.period,
            "publish_lag_days": self.publish_lag_days,
            "publisher": self.publisher,
            "source": self.source,
            "license": self.license,
            "license_url": self.license_url,
            "attribution": self.attribution,
            "url": self.url,
        }
        if self.ended_on:
            out["ended_on"] = self.ended_on.isoformat()
        if self.notes:
            out["notes"] = self.notes
        out.update(self.extra)
        return out


@dataclass(frozen=True)
class Series:
    """Readings sorted by timestamp, one per timestamp."""

    info: SeriesInfo
    timestamps: tuple[date, ...]
    values: tuple[float, ...]
    as_of: date | None = None  # when this copy of the series was taken

    def __post_init__(self) -> None:
        if len(self.timestamps) != len(self.values):
            raise ValueError("timestamps and values differ in length")
        if any(b <= a for a, b in zip(self.timestamps, self.timestamps[1:])):
            raise ValueError(f"{self.info.id}: timestamps must be strictly increasing")

    @property
    def id(self) -> str:
        return self.info.id

    def __len__(self) -> int:
        return len(self.timestamps)

    @classmethod
    def from_pairs(
        cls, info: SeriesInfo | str, pairs: Iterable[tuple[date | str, float]], as_of: date | None = None
    ) -> Series:
        if isinstance(info, str):
            info = SeriesInfo(id=info)
        rows: dict[date, float] = {}
        for t, v in pairs:
            d = t if isinstance(t, date) else date.fromisoformat(str(t)[:10])
            rows[d] = float(v)
        ts = tuple(sorted(rows))
        return cls(info=info, timestamps=ts, values=tuple(rows[t] for t in ts), as_of=as_of)

    def pairs(self) -> list[tuple[date, float]]:
        return list(zip(self.timestamps, self.values))

    def upto(self, cutoff: date) -> Series:
        """Readings dated on or before ``cutoff`` (what was knowable then, by timestamp)."""
        i = bisect.bisect_right(self.timestamps, cutoff)
        return replace(self, timestamps=self.timestamps[:i], values=self.values[:i])

    def last_on_or_before(self, d: date) -> tuple[date, float] | None:
        i = bisect.bisect_right(self.timestamps, d)
        return (self.timestamps[i - 1], self.values[i - 1]) if i else None

    def first_on_or_after(self, d: date) -> tuple[date, float] | None:
        i = bisect.bisect_left(self.timestamps, d)
        return (self.timestamps[i], self.values[i]) if i < len(self.timestamps) else None

    def nearest(self, d: date, tolerance_days: int) -> tuple[date, float] | None:
        """The reading closest to ``d`` within the tolerance (an exact date wins; ties go earlier)."""
        best: tuple[int, date, float] | None = None
        i = bisect.bisect_left(self.timestamps, d)
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(self.timestamps):
                gap = abs((self.timestamps[j] - d).days)
                if gap <= tolerance_days and (best is None or (gap, self.timestamps[j]) < (best[0], best[1])):
                    best = (gap, self.timestamps[j], self.values[j])
        return (best[1], best[2]) if best else None

    def merged(self, newer: Series) -> Series:
        """This series updated with ``newer``'s readings (newer wins on the same timestamp)."""
        rows = dict(self.pairs())
        rows.update(newer.pairs())
        return Series.from_pairs(self.info, rows.items(), as_of=newer.as_of or self.as_of)

    # ---- files -------------------------------------------------------------

    def to_csv(self) -> str:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["id", "timestamp", "target"])
        for t, v in self.pairs():
            w.writerow([self.id, t.isoformat(), _fmt(v)])
        return buf.getvalue()

    @classmethod
    def from_csv(cls, text: str, info: SeriesInfo | str | None = None, as_of: date | None = None) -> Series:
        rows = list(csv.DictReader(io.StringIO(text)))
        if rows and not {"timestamp", "target"} <= set(rows[0]):
            raise ValueError("series CSV needs timestamp and target columns (and optionally id)")
        sid = info if isinstance(info, str) else (info.id if info else (rows[0].get("id") if rows else "series"))
        inf = info if isinstance(info, SeriesInfo) else SeriesInfo(id=str(sid))
        return cls.from_pairs(inf, ((r["timestamp"], float(r["target"])) for r in rows if r["target"] != ""), as_of)


def _fmt(v: float) -> str:
    r = repr(float(v))
    return r[:-2] if r.endswith(".0") else r


def load_series_dir(directory: str | Path, manifest: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Series]:
    """Read every ``<id>.csv`` in a directory, with metadata from ``series.json`` if present."""
    import json

    d = Path(directory)
    meta: dict[str, SeriesInfo] = {}
    as_of: date | None = None
    mpath = d / "series.json"
    if manifest is None and mpath.exists():
        doc = json.loads(mpath.read_text(encoding="utf-8"))
        manifest = doc.get("series", [])
        if doc.get("as_of"):
            as_of = date.fromisoformat(doc["as_of"])
    for m in manifest or []:
        info = SeriesInfo.from_dict(m)
        meta[info.id] = info
    out: dict[str, Series] = {}
    for f in sorted(d.glob("*.csv")):
        sid = f.stem
        out[sid] = Series.from_csv(f.read_text(encoding="utf-8"), meta.get(sid, SeriesInfo(id=sid)), as_of)
    return out
