"""The text a forecaster is shown for a question, and parsing its answer.

The context lists readings dated on or before the call's ``cutoff`` only.
"""

from __future__ import annotations

import re

from ._meta import NAME
from .calls import Call, Forecast, parse_lag
from .resolve import apply_transform
from .series import Series

DEFAULT_CONTEXT = 24

_PROB = re.compile(r"PROBABILITY\s*[:=]\s*(\d+(?:\.\d+)?|\.\d+)\s*(%?)", re.I)
_VALUE = re.compile(r"VALUE\s*[:=]\s*\$?\s*(-?[\d,]*\.?\d+(?:[eE][-+]?\d+)?)", re.I)


_UNITS = {"D": "day", "W": "week", "M": "month", "Q": "quarter", "Y": "year"}


def lag_words(lag: str) -> str:
    """``"12M"`` → ``"12 months"``."""
    n, unit = parse_lag(lag)
    return f"{n} {_UNITS[unit]}{'' if n == 1 else 's'}"


def rule_text(call: Call) -> str:
    r = call.rule
    pick = (
        f"the latest reading dated on or before {call.deadline.isoformat()} (and no more than {r.gap_days} days before it)"
        if r.pick == "last_on_or_before"
        else f"the first reading dated on or after {call.deadline.isoformat()} (and no more than {r.gap_days} days after it)"
    )
    tr = r.transform
    lag = lag_words(tr.lag) if tr.lag else ""
    what = {
        "level": "the reading itself",
        "change": f"the reading minus the reading {lag} earlier",
        "pct_change": f"the percent change from the reading {lag} earlier",
        "annualized_pct_change": f"the percent change from the reading {lag} earlier, at an annual rate",
    }[tr.kind]
    s = f"Resolves on {pick}, using {what}, as published in series `{call.series_id}`."
    s += f" If no such reading is published within {r.grace_days} days after the deadline, the question is void."
    return s


def context_lines(call: Call, series: Series | None, n: int = DEFAULT_CONTEXT) -> list[str]:
    if series is None or call.cutoff is None:
        return []
    hist = series.upto(call.cutoff)
    tr = call.rule.transform
    rows = []
    start = max(0, len(hist) - n)
    for t, v in list(hist.pairs())[start:]:
        if tr.kind == "level":
            rows.append(f"{t.isoformat()}  {v:g}")
        else:
            x = apply_transform(hist, t, v, tr)
            rows.append(f"{t.isoformat()}  {v:g}  ->  {x[0]:.3f}" if x else f"{t.isoformat()}  {v:g}  ->  n/a (no reading {lag_words(tr.lag or '1M')} earlier)")
    return rows


def prompt(call: Call, series: Series | None = None, n_context: int = DEFAULT_CONTEXT) -> str:
    """The question as shown to a forecaster (no forecast, no resolution)."""
    parts = [
        f"{NAME} question {call.id}",
        f"Today is {call.made_on.isoformat()}.",
        "",
        call.question,
        "",
        rule_text(call),
    ]
    if series is not None:
        inf = series.info
        parts.append(f"Series: {inf.name or call.series_id}" + (f" ({inf.publisher})" if inf.publisher else "") + (f", unit: {inf.unit}" if inf.unit else "") + ".")
    lines = context_lines(call, series, n_context)
    if lines:
        head = "date  reading" if call.rule.transform.kind == "level" else "date  reading  ->  value in the question's terms"
        parts += ["", f"Readings published by {call.made_on.isoformat()} (latest {len(lines)}, oldest first):", head, *lines]
    parts.append("")
    if call.kind == "binary":
        parts.append("Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>")
    else:
        parts.append("Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>")
    return "\n".join(parts)


def parse_answer(text: str, kind: str) -> Forecast | None:
    """Read the last ``PROBABILITY:`` or ``VALUE:`` line from a reply. None if absent or out of range."""
    if kind == "binary":
        m = list(_PROB.finditer(text))
        if not m:
            return None
        x = float(m[-1].group(1))
        if m[-1].group(2) == "%":
            x /= 100.0
        return Forecast(probability=x) if 0.0 <= x <= 1.0 else None
    m = list(_VALUE.finditer(text))
    if not m:
        return None
    try:
        return Forecast(value=float(m[-1].group(1).replace(",", "")))
    except ValueError:
        return None
