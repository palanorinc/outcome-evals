"""Scoring resolved calls: Brier, log score, calibration, hit rate, and two baselines.

A scorer never returns a score for an unresolved call: ``score_call`` raises
``UnresolvedCallError`` for a pending or void call, and ``summarize`` counts
those calls separately and leaves them out of every average.

Baselines, computed on the same resolved calls:

- **no change**: the rule applied to the latest reading the forecaster could
  see (``anchor``). For a binary call that is a probability of 1 or 0; for a
  number call it is the anchor value.
- **base rate**: how often the rule held historically when the same rule was
  replayed from earlier readings (``base_rate``, set when the question is made;
  ``baselines.base_rate`` recomputes it from a series). For a number call it is
  the anchor plus the median historical change (``base_change``).

Log score is the natural log of the probability given to what happened
(higher is better; 0 is perfect). Probabilities are clipped to
[``EPS``, 1 − ``EPS``] so a confident miss costs ln(EPS), not infinity; the
same clip applies to the hard 0/1 no-change baseline.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from typing import Any

from .calls import Call, Forecast, Resolution

EPS = 1e-4
N_BINS = 10


class UnresolvedCallError(ValueError):
    """Raised when asked to score a call that is not resolved."""


def brier(p: float, outcome: bool) -> float:
    return (p - (1.0 if outcome else 0.0)) ** 2


def log_score(p: float, outcome: bool, eps: float = EPS) -> float:
    q = min(max(p if outcome else 1.0 - p, eps), 1.0 - eps)
    return math.log(q)


def hit(p: float, outcome: bool) -> float:
    """1 if the forecast leaned the right way, 0 if the wrong way, 0.5 at exactly 0.5."""
    if p == 0.5:
        return 0.5
    return 1.0 if (p > 0.5) == outcome else 0.0


def pinball(levels: Sequence[float], quantiles: Sequence[float], y: float) -> float:
    """Mean quantile (pinball) loss over the levels."""
    if not levels:
        raise ValueError("no quantiles")
    total = 0.0
    for q, x in zip(levels, quantiles):
        d = y - x
        total += max(q * d, (q - 1.0) * d)
    return total / len(levels)


@dataclass(frozen=True)
class CallScore:
    id: str
    kind: str
    outcome: bool | None = None
    value: float | None = None
    probability: float | None = None
    brier: float | None = None
    log_score: float | None = None
    hit: float | None = None
    forecast_value: float | None = None
    abs_error: float | None = None
    squared_error: float | None = None
    quantile_loss: float | None = None
    no_change: dict[str, float] = field(default_factory=dict)
    base_rate: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None and v != {}}


def _resolution(call: Call, resolution: Resolution | None) -> Resolution:
    r = resolution or call.resolution
    if r is None or not r.resolved or r.value is None:
        status = "no resolution" if r is None else r.status
        raise UnresolvedCallError(f"{call.id}: not resolved ({status}); unresolved calls are never scored")
    return r


def score_call(call: Call, forecast: Forecast | None = None, resolution: Resolution | None = None) -> CallScore:
    """Score one resolved call. Raises ``UnresolvedCallError`` if it is not resolved."""
    r = _resolution(call, resolution)
    f = forecast or call.forecast
    assert r.value is not None
    if call.kind == "binary":
        assert r.outcome is not None
        o = r.outcome
        nc: dict[str, float] = {}
        if call.anchor is not None:
            p0 = 1.0 if call.rule.holds(call.anchor.value) else 0.0
            nc = {"probability": p0, "brier": brier(p0, o), "log_score": log_score(p0, o), "hit": hit(p0, o)}
        br: dict[str, float] = {}
        if call.base_rate is not None:
            pb = call.base_rate
            br = {"probability": pb, "brier": brier(pb, o), "log_score": log_score(pb, o), "hit": hit(pb, o)}
        if f is None or f.probability is None:
            return CallScore(id=call.id, kind="binary", outcome=o, value=r.value, no_change=nc, base_rate=br)
        p = f.probability
        return CallScore(
            id=call.id, kind="binary", outcome=o, value=r.value, probability=p,
            brier=brier(p, o), log_score=log_score(p, o), hit=hit(p, o), no_change=nc, base_rate=br,
        )
    y = r.value
    nc = {}
    if call.anchor is not None:
        nc = {"value": call.anchor.value, "abs_error": abs(y - call.anchor.value)}
    br = {}
    if call.anchor is not None and call.base_change is not None:
        b = call.anchor.value + call.base_change
        br = {"value": b, "abs_error": abs(y - b)}
    if f is None:
        return CallScore(id=call.id, kind="number", value=y, no_change=nc, base_rate=br)
    ql = pinball(f.quantile_levels, f.quantiles, y) if f.quantiles else None
    point = f.value
    if point is None and f.quantiles:
        # the median, or the middle quantile, stands in for a point forecast
        point = f.quantiles[min(range(len(f.quantile_levels)), key=lambda i: abs(f.quantile_levels[i] - 0.5))]
    ae = abs(y - point) if point is not None else None
    return CallScore(
        id=call.id, kind="number", value=y, forecast_value=point, abs_error=ae,
        squared_error=None if ae is None else ae * ae, quantile_loss=ql, no_change=nc, base_rate=br,
    )


@dataclass(frozen=True)
class CalibrationBin:
    lower: float
    upper: float
    n: int
    mean_probability: float | None
    observed_frequency: float | None


def calibration(pairs: Iterable[tuple[float, bool]], n_bins: int = N_BINS) -> list[CalibrationBin]:
    """Equal-width bins over [0, 1]; a probability of exactly 1 goes in the top bin."""
    bins: list[list[tuple[float, bool]]] = [[] for _ in range(n_bins)]
    for p, o in pairs:
        bins[min(int(p * n_bins), n_bins - 1)].append((p, o))
    out = []
    for i, b in enumerate(bins):
        out.append(
            CalibrationBin(
                lower=i / n_bins,
                upper=(i + 1) / n_bins,
                n=len(b),
                mean_probability=statistics.fmean(p for p, _ in b) if b else None,
                observed_frequency=statistics.fmean(1.0 if o else 0.0 for _, o in b) if b else None,
            )
        )
    return out


def _mean(xs: Sequence[float]) -> float | None:
    return statistics.fmean(xs) if xs else None


@dataclass
class Summary:
    """Scores over a set of calls. Unresolved calls are counted, never scored."""

    n_calls: int = 0
    n_resolved: int = 0
    n_pending: int = 0
    n_void: int = 0
    n_unforecast: int = 0
    binary: dict[str, Any] = field(default_factory=dict)
    number: dict[str, Any] = field(default_factory=dict)
    calibration: list[CalibrationBin] = field(default_factory=list)
    scores: list[CallScore] = field(default_factory=list)

    def to_dict(self, include_scores: bool = False) -> dict[str, Any]:
        d: dict[str, Any] = {
            "n_calls": self.n_calls,
            "n_resolved": self.n_resolved,
            "n_pending": self.n_pending,
            "n_void": self.n_void,
            "n_resolved_without_forecast": self.n_unforecast,
            "binary": self.binary,
            "number": self.number,
            "calibration": [asdict(b) for b in self.calibration if b.n],
        }
        if include_scores:
            d["scores"] = [s.to_dict() for s in self.scores]
        return d

    def text(self) -> str:
        """A short plain-text report."""
        lines = [
            f"calls: {self.n_calls} · resolved: {self.n_resolved} · pending: {self.n_pending} · void: {self.n_void}"
            + (f" · resolved without a forecast: {self.n_unforecast}" if self.n_unforecast else "")
        ]
        b = self.binary
        if b.get("n"):
            lines.append(f"yes/no calls scored: {b['n']}")
            lines.append(
                f"  {'':<12}{'Brier':>8}{'log score':>11}{'hit rate':>10}"
            )
            for label, key in (("forecast", "forecast"), ("no change", "no_change"), ("base rate", "base_rate")):
                m = b.get(key) or {}
                if m.get("n"):
                    lines.append(
                        f"  {label:<12}{m['brier']:>8.3f}{m['log_score']:>11.3f}{m['hit_rate']:>10.1%}"
                        + ("" if m["n"] == b["n"] else f"   (n={m['n']})")
                    )
        n = self.number
        if n.get("n"):
            lines.append(f"number calls scored: {n['n']}")
            for label, key in (("forecast", "forecast"), ("no change", "no_change"), ("base rate", "base_rate")):
                m = n.get(key) or {}
                if m.get("n"):
                    extra = f"   skill vs no change {m['skill_vs_no_change']:+.1%}" if m.get("skill_vs_no_change") is not None else ""
                    lines.append(f"  {label:<12}mean scaled abs error {m['mean_scaled_abs_error']:.3f}{extra}")
        if any(c.n for c in self.calibration):
            lines.append("calibration (forecast probability → how often it happened):")
            for c in self.calibration:
                if c.n:
                    assert c.mean_probability is not None and c.observed_frequency is not None
                    lines.append(
                        f"  {c.lower:.1f}–{c.upper:.1f}: n={c.n:<5} said {c.mean_probability:.2f}, happened {c.observed_frequency:.2f}"
                    )
        return "\n".join(lines)


def _scale(call: Call) -> float:
    """The error scale for a number call: its ``scale`` (the median absolute move over the
    same horizon in the series' history), so errors in different units can be averaged. 1 if absent."""
    return call.scale if call.scale else 1.0


def summarize(calls: Sequence[Call], forecasts: dict[str, Forecast] | None = None) -> Summary:
    """Score every resolved call that has a forecast (from ``forecasts`` or the call itself)."""
    s = Summary(n_calls=len(calls))
    bin_f: dict[str, list[float]] = {"brier": [], "log_score": [], "hit": []}
    bin_nc: dict[str, list[float]] = {"brier": [], "log_score": [], "hit": []}
    bin_br: dict[str, list[float]] = {"brier": [], "log_score": [], "hit": []}
    num_f: list[float] = []
    num_nc_matched: list[tuple[float, float]] = []
    num_nc: list[float] = []
    num_br: list[float] = []
    abs_err: list[float] = []
    sq_err: list[float] = []
    qloss: list[float] = []
    cal: list[tuple[float, bool]] = []
    for c in calls:
        r = c.resolution
        if r is None or r.status == "pending":
            s.n_pending += 1
            continue
        if r.status == "void":
            s.n_void += 1
            continue
        s.n_resolved += 1
        f = (forecasts or {}).get(c.id) or c.forecast
        if f is None:
            s.n_unforecast += 1
            continue
        cs = score_call(c, f)
        s.scores.append(cs)
        if cs.kind == "binary" and cs.brier is not None:
            assert cs.log_score is not None and cs.hit is not None and cs.probability is not None and cs.outcome is not None
            bin_f["brier"].append(cs.brier)
            bin_f["log_score"].append(cs.log_score)
            bin_f["hit"].append(cs.hit)
            cal.append((cs.probability, cs.outcome))
            for src, dst in ((cs.no_change, bin_nc), (cs.base_rate, bin_br)):
                if src:
                    for k in dst:
                        dst[k].append(src[k])
        elif cs.kind == "number" and cs.abs_error is not None:
            sc = _scale(c)
            num_f.append(cs.abs_error / sc)
            abs_err.append(cs.abs_error)
            sq_err.append(cs.abs_error**2)
            if cs.quantile_loss is not None:
                qloss.append(cs.quantile_loss / sc)
            if cs.no_change:
                num_nc.append(cs.no_change["abs_error"] / sc)
                num_nc_matched.append((cs.abs_error / sc, cs.no_change["abs_error"] / sc))
            if cs.base_rate:
                num_br.append(cs.base_rate["abs_error"] / sc)

    def bsum(d: dict[str, list[float]]) -> dict[str, Any]:
        if not d["brier"]:
            return {"n": 0}
        return {
            "n": len(d["brier"]),
            "brier": statistics.fmean(d["brier"]),
            "log_score": statistics.fmean(d["log_score"]),
            "hit_rate": statistics.fmean(d["hit"]),
        }

    nb = len(bin_f["brier"])
    if nb:
        s.binary = {"n": nb, "forecast": bsum(bin_f), "no_change": bsum(bin_nc), "base_rate": bsum(bin_br)}
        s.calibration = calibration(cal)
    nn = len(num_f)
    if nn:
        nc_mean = _mean([b for _, b in num_nc_matched])
        f_matched = _mean([a for a, _ in num_nc_matched])
        skill = None if not nc_mean or f_matched is None else 1.0 - f_matched / nc_mean
        s.number = {
            "n": nn,
            "forecast": {
                "n": nn,
                "mean_scaled_abs_error": statistics.fmean(num_f),
                "mean_abs_error": statistics.fmean(abs_err),
                "rmse": math.sqrt(statistics.fmean(sq_err)),
                "skill_vs_no_change": skill,
                **({"mean_scaled_quantile_loss": statistics.fmean(qloss)} if qloss else {}),
            },
            "no_change": {"n": len(num_nc), "mean_scaled_abs_error": _mean(num_nc)} if num_nc else {"n": 0},
            "base_rate": {"n": len(num_br), "mean_scaled_abs_error": _mean(num_br)} if num_br else {"n": 0},
            "note": "scaled errors are divided by each call's scale (the median absolute historical move over the same horizon) so series in different units can be averaged",
        }
    return s
