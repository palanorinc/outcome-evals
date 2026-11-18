"""The call format: a dated question about a public series, with or without a forecast.

A *question* says what will be checked, against which series, by when and by
what rule. A *call* is a question plus somebody's forecast. Both use the same
record; ``forecast`` is simply absent on a bare question. The JSON Schema is in
``outcome_evals/schema/call.schema.json`` and ``validate_dict`` checks against
the same rules without needing ``jsonschema``.

Dates are ISO dates (``YYYY-MM-DD``). Field names shared with the ``fev``
forecasting-evaluation format mean the same thing there: ``cutoff`` is the last
series timestamp a forecaster may see, ``quantile_levels`` are the levels of a
quantile forecast, and the series files use ``id``, ``timestamp`` and ``target``
columns.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Any

KINDS = ("binary", "number")
COMPARATORS = (">", ">=", "<", "<=", "between")
PICKS = ("last_on_or_before", "first_on_or_after")
PERIODS = ("D", "B", "W", "M", "Q", "A")
TRANSFORMS = ("level", "change", "pct_change", "annualized_pct_change")
STATUSES = ("resolved", "pending", "void")
SPLITS = ("live", "resolved_history", "private")

# How far before the deadline a reading may be dated and still count, by cadence.
DEFAULT_MAX_GAP_DAYS = {"D": 5, "B": 5, "W": 8, "M": 31, "Q": 92, "A": 366}


class CallFormatError(ValueError):
    """A call or question does not follow the format."""


def _date(v: Any, name: str) -> date:
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        try:
            return date.fromisoformat(v[:10])
        except ValueError as e:
            raise CallFormatError(f"{name}: not an ISO date: {v!r}") from e
    raise CallFormatError(f"{name}: expected an ISO date string, got {type(v).__name__}")


def _opt_date(v: Any, name: str) -> date | None:
    return None if v is None else _date(v, name)


def _num(v: Any, name: str) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise CallFormatError(f"{name}: expected a number, got {v!r}")
    f = float(v)
    if not math.isfinite(f):
        raise CallFormatError(f"{name}: must be finite")
    return f


def _opt_num(v: Any, name: str) -> float | None:
    return None if v is None else _num(v, name)


def _choice(v: Any, allowed: Sequence[str], name: str) -> str:
    if v not in allowed:
        raise CallFormatError(f"{name}: {v!r} is not one of {', '.join(allowed)}")
    return str(v)


def _drop_none(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None and v != [] and v != {}}


@dataclass(frozen=True)
class Transform:
    """What is compared: the reading itself, or its change against an earlier reading.

    ``lag`` is a calendar offset such as ``"1M"``, ``"12M"``, ``"1Q"``, ``"7D"``,
    ``"1W"`` or ``"1Y"``. The earlier reading must be dated within
    ``tolerance_days`` of (reading date − lag); otherwise the call is void.
    """

    kind: str = "level"
    lag: str | None = None
    tolerance_days: int = 3

    def __post_init__(self) -> None:
        _choice(self.kind, TRANSFORMS, "rule.transform.kind")
        if self.kind != "level":
            if not self.lag:
                raise CallFormatError(f"rule.transform.lag is required for {self.kind}")
            parse_lag(self.lag)
        if self.tolerance_days < 0:
            raise CallFormatError("rule.transform.tolerance_days must be ≥ 0")

    @classmethod
    def from_dict(cls, d: Mapping[str, Any] | None) -> Transform:
        if d is None:
            return cls()
        return cls(
            kind=d.get("kind", "level"),
            lag=d.get("lag"),
            tolerance_days=int(d.get("tolerance_days", 3)),
        )

    def to_dict(self) -> dict[str, Any]:
        if self.kind == "level":
            return {"kind": "level"}
        out: dict[str, Any] = {"kind": self.kind, "lag": self.lag}
        if self.tolerance_days != 3:
            out["tolerance_days"] = self.tolerance_days
        return out


def parse_lag(lag: str) -> tuple[int, str]:
    """``"12M"`` → ``(12, "M")``. Units: D, W, M, Q, Y."""
    s = lag.strip().upper()
    if len(s) < 2 or s[-1] not in "DWMQY" or not s[:-1].isdigit() or int(s[:-1]) <= 0:
        raise CallFormatError(f"lag: {lag!r} is not like 1M, 12M, 1Q, 7D, 1W or 1Y")
    return int(s[:-1]), s[-1]


@dataclass(frozen=True)
class Rule:
    """How the deadline reading is chosen and judged.

    - ``pick``: ``last_on_or_before`` takes the latest reading dated on or before
      the deadline and no more than ``max_gap_days`` before it;
      ``first_on_or_after`` takes the first reading dated on or after the deadline
      and no more than ``max_gap_days`` after it.
    - ``period``: the series' cadence (D daily, B business days, W, M, Q, A). It
      tells the resolver when a reading is final: the next reading would be
      dated after the deadline.
    - ``grace_days``: how long after the deadline to wait for a late or missing
      publication before resolving on what exists, or voiding.
    - binary calls: ``comparator`` with ``threshold``, or ``between`` with
      ``low`` (inclusive) and ``high`` (exclusive).
    """

    comparator: str | None = None
    threshold: float | None = None
    low: float | None = None
    high: float | None = None
    pick: str = "last_on_or_before"
    period: str = "M"
    max_gap_days: int | None = None
    grace_days: int = 60
    transform: Transform = field(default_factory=Transform)
    threshold_basis: str | None = None

    def __post_init__(self) -> None:
        _choice(self.pick, PICKS, "rule.pick")
        _choice(self.period, PERIODS, "rule.period")
        if self.comparator is not None:
            _choice(self.comparator, COMPARATORS, "rule.comparator")
            if self.comparator == "between":
                if self.low is None or self.high is None:
                    raise CallFormatError("rule: 'between' needs low and high")
                if not self.low < self.high:
                    raise CallFormatError("rule: low must be below high")
            elif self.threshold is None:
                raise CallFormatError(f"rule: comparator {self.comparator!r} needs a threshold")
        if self.max_gap_days is not None and self.max_gap_days < 0:
            raise CallFormatError("rule.max_gap_days must be ≥ 0")
        if self.grace_days < 0:
            raise CallFormatError("rule.grace_days must be ≥ 0")

    @property
    def gap_days(self) -> int:
        return self.max_gap_days if self.max_gap_days is not None else DEFAULT_MAX_GAP_DAYS[self.period]

    def holds(self, x: float) -> bool:
        """Whether a (transformed) value satisfies the binary rule."""
        x = round(x, 9)
        c = self.comparator
        if c == "between":
            assert self.low is not None and self.high is not None
            return self.low <= x < self.high
        assert self.threshold is not None
        t = self.threshold
        if c == ">":
            return x > t
        if c == ">=":
            return x >= t
        if c == "<":
            return x < t
        if c == "<=":
            return x <= t
        raise CallFormatError(f"rule has no comparator: {c!r}")

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Rule:
        if not isinstance(d, Mapping):
            raise CallFormatError("rule: expected an object")
        return cls(
            comparator=d.get("comparator"),
            threshold=_opt_num(d.get("threshold"), "rule.threshold"),
            low=_opt_num(d.get("low"), "rule.low"),
            high=_opt_num(d.get("high"), "rule.high"),
            pick=d.get("pick", "last_on_or_before"),
            period=d.get("period", "M"),
            max_gap_days=None if d.get("max_gap_days") is None else int(d["max_gap_days"]),
            grace_days=int(d.get("grace_days", 60)),
            transform=Transform.from_dict(d.get("transform")),
            threshold_basis=d.get("threshold_basis"),
        )

    def to_dict(self) -> dict[str, Any]:
        return _drop_none(
            {
                "comparator": self.comparator,
                "threshold": self.threshold,
                "low": self.low,
                "high": self.high,
                "pick": self.pick,
                "period": self.period,
                "max_gap_days": self.max_gap_days,
                "grace_days": self.grace_days,
                "transform": self.transform.to_dict(),
                "threshold_basis": self.threshold_basis,
            }
        )


@dataclass(frozen=True)
class Forecast:
    """A forecast: a probability (binary) or a value, optionally with quantiles (number)."""

    probability: float | None = None
    value: float | None = None
    quantile_levels: tuple[float, ...] = ()
    quantiles: tuple[float, ...] = ()
    forecaster: str | None = None

    def __post_init__(self) -> None:
        if self.probability is not None and not 0.0 <= self.probability <= 1.0:
            raise CallFormatError("forecast.probability must be between 0 and 1")
        if len(self.quantile_levels) != len(self.quantiles):
            raise CallFormatError("forecast.quantiles must match forecast.quantile_levels")
        if any(not 0.0 < q < 1.0 for q in self.quantile_levels):
            raise CallFormatError("forecast.quantile_levels must be strictly between 0 and 1")

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Forecast:
        return cls(
            probability=_opt_num(d.get("probability"), "forecast.probability"),
            value=_opt_num(d.get("value"), "forecast.value"),
            quantile_levels=tuple(_num(x, "forecast.quantile_levels") for x in d.get("quantile_levels", ())),
            quantiles=tuple(_num(x, "forecast.quantiles") for x in d.get("quantiles", ())),
            forecaster=d.get("forecaster"),
        )

    def to_dict(self) -> dict[str, Any]:
        return _drop_none(
            {
                "probability": self.probability,
                "value": self.value,
                "quantile_levels": list(self.quantile_levels),
                "quantiles": list(self.quantiles),
                "forecaster": self.forecaster,
            }
        )


@dataclass(frozen=True)
class Anchor:
    """The latest reading a forecaster could see, in the rule's units (after the transform)."""

    timestamp: date
    value: float

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Anchor:
        return cls(timestamp=_date(d.get("timestamp"), "anchor.timestamp"), value=_num(d.get("value"), "anchor.value"))

    def to_dict(self) -> dict[str, Any]:
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}


@dataclass(frozen=True)
class Resolution:
    """What the resolver found. ``value`` is in the rule's units; ``reading_value`` is the raw reading."""

    status: str
    as_of: date
    reason: str = ""
    reading_timestamp: date | None = None
    reading_value: float | None = None
    comparison_timestamp: date | None = None
    comparison_value: float | None = None
    value: float | None = None
    outcome: bool | None = None
    revisions: tuple[dict[str, Any], ...] = ()

    def __post_init__(self) -> None:
        _choice(self.status, STATUSES, "resolution.status")
        if self.status == "resolved" and self.value is None:
            raise CallFormatError("a resolved resolution needs a value")

    @property
    def resolved(self) -> bool:
        return self.status == "resolved"

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Resolution:
        oc = d.get("outcome")
        return cls(
            status=d.get("status", ""),
            as_of=_date(d.get("as_of"), "resolution.as_of"),
            reason=d.get("reason", ""),
            reading_timestamp=_opt_date(d.get("reading_timestamp"), "resolution.reading_timestamp"),
            reading_value=_opt_num(d.get("reading_value"), "resolution.reading_value"),
            comparison_timestamp=_opt_date(d.get("comparison_timestamp"), "resolution.comparison_timestamp"),
            comparison_value=_opt_num(d.get("comparison_value"), "resolution.comparison_value"),
            value=_opt_num(d.get("value"), "resolution.value"),
            outcome=None if oc is None else bool(oc),
            revisions=tuple(d.get("revisions", ())),
        )

    def to_dict(self) -> dict[str, Any]:
        return _drop_none(
            {
                "status": self.status,
                "as_of": self.as_of.isoformat(),
                "reason": self.reason or None,
                "reading_timestamp": self.reading_timestamp.isoformat() if self.reading_timestamp else None,
                "reading_value": self.reading_value,
                "comparison_timestamp": self.comparison_timestamp.isoformat() if self.comparison_timestamp else None,
                "comparison_value": self.comparison_value,
                "value": self.value,
                "outcome": self.outcome,
                "revisions": list(self.revisions),
            }
        )


@dataclass(frozen=True)
class Call:
    """A dated question about a public series, optionally carrying a forecast and a resolution."""

    id: str
    question: str
    kind: str
    made_on: date
    deadline: date
    series_id: str
    rule: Rule
    source: str
    license: str
    unit: str | None = None
    split: str | None = None
    cutoff: date | None = None
    anchor: Anchor | None = None
    base_rate: float | None = None
    base_change: float | None = None
    scale: float | None = None
    tags: tuple[str, ...] = ()
    forecast: Forecast | None = None
    resolution: Resolution | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.id or not isinstance(self.id, str):
            raise CallFormatError("id is required")
        if not self.question.strip():
            raise CallFormatError(f"{self.id}: question is required")
        _choice(self.kind, KINDS, f"{self.id}: kind")
        if self.split is not None:
            _choice(self.split, SPLITS, f"{self.id}: split")
        if self.deadline < self.made_on:
            raise CallFormatError(f"{self.id}: deadline is before made_on")
        if self.cutoff is not None and self.cutoff > self.made_on:
            raise CallFormatError(f"{self.id}: cutoff is after made_on (look-ahead)")
        if self.kind == "binary" and self.rule.comparator is None:
            raise CallFormatError(f"{self.id}: a binary call needs rule.comparator")
        if self.kind == "number" and self.rule.comparator is not None:
            raise CallFormatError(f"{self.id}: a number call takes no comparator")
        if self.scale is not None and self.scale <= 0:
            raise CallFormatError(f"{self.id}: scale must be positive")
        if self.base_rate is not None and not 0.0 <= self.base_rate <= 1.0:
            raise CallFormatError(f"{self.id}: base_rate must be between 0 and 1")
        if self.forecast is not None:
            if self.kind == "binary" and self.forecast.probability is None:
                raise CallFormatError(f"{self.id}: a binary call's forecast needs a probability")
            if self.kind == "number" and self.forecast.value is None and not self.forecast.quantiles:
                raise CallFormatError(f"{self.id}: a number call's forecast needs a value or quantiles")
        if not self.series_id:
            raise CallFormatError(f"{self.id}: series_id is required")

    @property
    def horizon_days(self) -> int:
        return (self.deadline - self.made_on).days

    def with_forecast(self, forecast: Forecast) -> Call:
        return replace(self, forecast=forecast)

    def with_resolution(self, resolution: Resolution | None) -> Call:
        return replace(self, resolution=resolution)

    def question_only(self) -> Call:
        """The call without its forecast or resolution (what a forecaster is shown)."""
        return replace(self, forecast=None, resolution=None)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Call:
        if not isinstance(d, Mapping):
            raise CallFormatError("a call must be a JSON object")
        unknown = set(d) - _FIELDS
        if unknown:
            raise CallFormatError(f"{d.get('id', '?')}: unknown field(s): {', '.join(sorted(unknown))}")
        for req in ("id", "question", "kind", "made_on", "deadline", "series_id", "rule", "source", "license"):
            if d.get(req) in (None, ""):
                raise CallFormatError(f"{d.get('id', '?')}: missing {req}")
        return cls(
            id=str(d["id"]),
            question=str(d["question"]),
            kind=d["kind"],
            made_on=_date(d["made_on"], "made_on"),
            deadline=_date(d["deadline"], "deadline"),
            series_id=str(d["series_id"]),
            rule=Rule.from_dict(d["rule"]),
            source=str(d["source"]),
            license=str(d["license"]),
            unit=d.get("unit"),
            split=d.get("split"),
            cutoff=_opt_date(d.get("cutoff"), "cutoff"),
            anchor=Anchor.from_dict(d["anchor"]) if d.get("anchor") else None,
            base_rate=_opt_num(d.get("base_rate"), "base_rate"),
            base_change=_opt_num(d.get("base_change"), "base_change"),
            scale=_opt_num(d.get("scale"), "scale"),
            tags=tuple(d.get("tags", ())),
            forecast=Forecast.from_dict(d["forecast"]) if d.get("forecast") else None,
            resolution=Resolution.from_dict(d["resolution"]) if d.get("resolution") else None,
            notes=d.get("notes"),
        )

    def to_dict(self) -> dict[str, Any]:
        return _drop_none(
            {
                "id": self.id,
                "question": self.question,
                "kind": self.kind,
                "made_on": self.made_on.isoformat(),
                "deadline": self.deadline.isoformat(),
                "series_id": self.series_id,
                "rule": self.rule.to_dict(),
                "source": self.source,
                "license": self.license,
                "unit": self.unit,
                "split": self.split,
                "cutoff": self.cutoff.isoformat() if self.cutoff else None,
                "anchor": self.anchor.to_dict() if self.anchor else None,
                "base_rate": self.base_rate,
                "base_change": self.base_change,
                "scale": self.scale,
                "tags": list(self.tags),
                "forecast": self.forecast.to_dict() if self.forecast else None,
                "resolution": self.resolution.to_dict() if self.resolution else None,
                "notes": self.notes,
            }
        )


_FIELDS = {
    "id", "question", "kind", "made_on", "deadline", "series_id", "rule", "source", "license", "unit", "split",
    "cutoff", "anchor", "base_rate", "base_change", "scale", "tags", "forecast", "resolution", "notes", "horizon_days",
}


def validate_dict(d: Mapping[str, Any]) -> list[str]:
    """Problems with one call record, as messages. Empty when the record is valid."""
    try:
        Call.from_dict(d)
    except CallFormatError as e:
        return [str(e)]
    return []


def iter_calls(path: str | Path) -> Iterator[Call]:
    """Read calls from a ``.jsonl`` file (one per line) or a ``.json`` file (a list)."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict) and "calls" in data:
            data = data["calls"]
        if not isinstance(data, list):
            raise CallFormatError(f"{p}: expected a list of calls")
        for d in data:
            yield Call.from_dict(d)
        return
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip():
            try:
                yield Call.from_dict(json.loads(line))
            except (CallFormatError, json.JSONDecodeError) as e:
                raise CallFormatError(f"{p}:{n}: {e}") from e


def load_calls(*paths: str | Path) -> list[Call]:
    out: list[Call] = []
    for p in paths:
        out.extend(iter_calls(p))
    ids = [c.id for c in out]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise CallFormatError(f"duplicate call ids: {', '.join(sorted(dupes)[:5])}")
    return out


def dump_calls(calls: Iterable[Call], path: str | Path) -> None:
    """Write calls as ``.jsonl`` (one compact JSON object per line, stable key order)."""
    lines = [json.dumps(c.to_dict(), ensure_ascii=False, separators=(",", ":")) for c in calls]
    Path(path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
