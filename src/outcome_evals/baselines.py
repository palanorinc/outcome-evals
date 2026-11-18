"""Anchors and baselines, computed only from readings a forecaster could have seen.

``context`` cuts a series at a call's ``cutoff``. Everything here reads that
cut series and nothing later, so the baselines carry no look-ahead.

The base rate replays the call's own rule from earlier starting points: for
every reading in the look-back window, move forward by the same distance as
from the anchor to the deadline, choose the reading the same way, and record
the change. The share of those changes that would have satisfied the rule,
added to today's anchor, is the base rate.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, replace
from datetime import date, timedelta

from .calls import Anchor, Call, Rule
from .resolve import apply_transform, select_reading
from .series import Series

MIN_HISTORY = 24
DEFAULT_LOOKBACK_YEARS = 10


def context(series: Series, cutoff: date) -> Series:
    """The series as a forecaster saw it: readings dated on or before ``cutoff``."""
    return series.upto(cutoff)


def anchor_at(series: Series, cutoff: date, rule: Rule) -> Anchor | None:
    """The latest reading on or before ``cutoff``, in the rule's units."""
    hist = series.upto(cutoff)
    for i in range(len(hist) - 1, max(-1, len(hist) - 6), -1):
        t, v = hist.timestamps[i], hist.values[i]
        tv = apply_transform(hist, t, v, rule.transform)
        if tv is not None:
            return Anchor(timestamp=t, value=round(tv[0], 9))
    return None


@dataclass(frozen=True)
class History:
    changes: tuple[float, ...]
    anchor: Anchor

    @property
    def n(self) -> int:
        return len(self.changes)

    def base_rate(self, rule: Rule) -> float | None:
        if self.n < MIN_HISTORY or rule.comparator is None:
            return None
        return sum(1 for ch in self.changes if rule.holds(self.anchor.value + ch)) / self.n

    def base_change(self) -> float | None:
        return statistics.median(self.changes) if self.n >= MIN_HISTORY else None

    def scale(self) -> float | None:
        if self.n < MIN_HISTORY:
            return None
        absd = [abs(c) for c in self.changes]
        m = statistics.median(absd)
        if m > 0:
            return m
        mean = statistics.fmean(absd)
        return mean if mean > 0 else None

    def quantile(self, q: float) -> float:
        xs = sorted(self.changes)
        if not xs:
            raise ValueError("no history")
        pos = q * (len(xs) - 1)
        lo = int(pos)
        hi = min(lo + 1, len(xs) - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def history(
    series: Series, cutoff: date, deadline: date, rule: Rule, lookback_years: int = DEFAULT_LOOKBACK_YEARS
) -> History | None:
    """Historical changes from a reading to the reading the same rule picks at the same distance."""
    hist = series.upto(cutoff)
    anc = anchor_at(hist, cutoff, rule)
    if anc is None:
        return None
    offset = deadline - anc.timestamp
    start = date(cutoff.year - lookback_years, cutoff.month, min(cutoff.day, 28))
    changes: list[float] = []
    # a quiet rule: no grace fallback inside the replay, only clean picks
    replay_rule = replace(rule, grace_days=0)
    for t, v in hist.pairs():
        if t < start:
            continue
        d_i = t + offset
        if d_i >= cutoff:
            break
        x = apply_transform(hist, t, v, rule.transform)
        if x is None:
            continue
        status, reading, _ = select_reading(hist, d_i, replay_rule, cutoff)
        if status != "resolved" or reading is None:
            continue
        y = apply_transform(hist, reading[0], reading[1], rule.transform)
        if y is None:
            continue
        changes.append(y[0] - x[0])
    return History(changes=tuple(changes), anchor=anc)


def with_baselines(call: Call, series: Series, lookback_years: int = DEFAULT_LOOKBACK_YEARS) -> Call:
    """Fill ``anchor``, ``base_rate`` (binary), ``base_change`` and ``scale`` from the series at the call's cutoff.

    The cutoff defaults to ``made_on − publish_lag_days`` of the series: the
    last date whose reading would already have been published.
    """
    cutoff = call.cutoff
    if cutoff is None:
        bound = call.made_on - timedelta(days=series.info.publish_lag_days)
        last = series.last_on_or_before(bound)
        cutoff = last[0] if last else bound
    h = history(series, cutoff, call.deadline, call.rule, lookback_years)
    if h is None:
        return replace(call, cutoff=cutoff)
    return replace(
        call,
        cutoff=cutoff,
        anchor=call.anchor or h.anchor,
        base_rate=call.base_rate if call.base_rate is not None else (h.base_rate(call.rule) if call.kind == "binary" else None),
        base_change=call.base_change if call.base_change is not None else h.base_change(),
        scale=call.scale or h.scale(),
    )
