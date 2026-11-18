"""The resolver: a pure function from a call and a dated series to resolved, not yet, or void.

Rules (each one is tested in ``tests/test_resolve.py``):

1. **Before the deadline** a call is always ``pending``.
2. **Choosing the reading.** ``last_on_or_before`` takes the latest reading
   dated in ``[deadline − max_gap_days, deadline]``; ``first_on_or_after`` takes
   the first reading dated in ``[deadline, deadline + max_gap_days]``.
3. **When it is final.** A ``last_on_or_before`` reading is final once a later
   reading exists, or once the next reading by the series' cadence would be
   dated after the deadline (the December figure is final for a 18 December
   deadline as soon as it is published). Until then the call is ``pending``.
4. **A missing reading on the deadline.** If no reading falls in the window,
   the call stays ``pending`` until ``grace_days`` after the deadline (late
   publications happen: a shutdown delayed U.S. releases in 2025), then it is
   ``void``. It is void at once if a later reading already exists, because the
   gap is then permanent (an October 2025 CPI figure was never published).
   After the grace period a ``last_on_or_before`` call resolves on the latest
   reading in its window even if the cadence says another could still come.
5. **A series that ends.** If the series' ``ended_on`` is before the start of
   the window, the call is ``void``.
6. **Transforms.** ``change``, ``pct_change`` and ``annualized_pct_change``
   compare the chosen reading with the reading dated at (reading date − lag),
   within ``tolerance_days``. No such reading → ``void``.
7. **Revisions.** The resolver reads whatever copy of the series it is given,
   so a revised series can give a different value. ``record`` keeps the first
   resolution: once a call is resolved, a later resolution from revised data
   does not change the outcome; the new value is appended to ``revisions``.
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

from .calls import Call, Resolution, Rule, Transform, parse_lag
from .series import Series


def add_months(d: date, months: int) -> date:
    y, m = divmod(d.month - 1 + months, 12)
    y += d.year
    m += 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def shift(d: date, n: int, unit: str) -> date:
    """Move a date by ``n`` units (D, B, W, M, Q, Y/A). Negative ``n`` moves back."""
    if unit == "D":
        return d + timedelta(days=n)
    if unit == "B":
        step = 1 if n >= 0 else -1
        out = d
        for _ in range(abs(n)):
            out += timedelta(days=step)
            while out.weekday() >= 5:
                out += timedelta(days=step)
        return out
    if unit == "W":
        return d + timedelta(weeks=n)
    if unit == "M":
        return add_months(d, n)
    if unit == "Q":
        return add_months(d, 3 * n)
    if unit in ("Y", "A"):
        return add_months(d, 12 * n)
    raise ValueError(f"unknown unit {unit!r}")


def next_period(d: date, period: str) -> date:
    return shift(d, 1, period)


_PER_YEAR = {"D": 365.25, "W": 365.25 / 7, "M": 12.0, "Q": 4.0, "Y": 1.0}


def apply_transform(series: Series, t: date, v: float, tr: Transform) -> tuple[float, date | None, float | None] | None:
    """The transformed value at reading ``(t, v)`` and the comparison reading used. None when missing."""
    if tr.kind == "level":
        return v, None, None
    assert tr.lag is not None
    n, unit = parse_lag(tr.lag)
    back = shift(t, -n, unit)
    comp = series.nearest(back, tr.tolerance_days)
    if comp is None or comp[0] >= t:
        return None
    ct, cv = comp
    if tr.kind == "change":
        return v - cv, ct, cv
    if cv == 0:
        return None
    if tr.kind == "pct_change":
        return (v / cv - 1.0) * 100.0, ct, cv
    if tr.kind == "annualized_pct_change":
        ratio = v / cv
        if ratio <= 0:
            return None
        return (ratio ** (_PER_YEAR[unit] / n) - 1.0) * 100.0, ct, cv
    raise ValueError(tr.kind)


def select_reading(series: Series, deadline: date, rule: Rule, as_of: date) -> tuple[str, tuple[date, float] | None, str]:
    """``("resolved"|"pending"|"void", reading, reason)`` for the deadline reading, before any transform."""
    gap = rule.gap_days
    grace_over = as_of > deadline + timedelta(days=rule.grace_days)
    if rule.pick == "last_on_or_before":
        lo = deadline - timedelta(days=gap)
        if series.info.ended_on is not None and series.info.ended_on < lo:
            return "void", None, f"series ended on {series.info.ended_on.isoformat()}"
        cand = series.last_on_or_before(deadline)
        if cand is not None and cand[0] < lo:
            cand = None
        later = series.first_on_or_after(deadline + timedelta(days=1))
        if cand is None:
            if later is not None:
                return "void", None, f"no reading dated {lo.isoformat()}–{deadline.isoformat()}, and a later reading exists"
            if grace_over:
                return "void", None, f"no reading dated {lo.isoformat()}–{deadline.isoformat()} within {rule.grace_days} days after the deadline"
            return "pending", None, "the deadline reading is not published yet"
        final = later is not None or next_period(cand[0], rule.period) > deadline or grace_over
        if not final:
            return "pending", cand, "a reading dated closer to the deadline may still be published"
        return "resolved", cand, ""
    # first_on_or_after
    hi = deadline + timedelta(days=gap)
    if series.info.ended_on is not None and series.info.ended_on < deadline:
        return "void", None, f"series ended on {series.info.ended_on.isoformat()}"
    cand = series.first_on_or_after(deadline)
    if cand is not None and cand[0] > hi:
        return "void", None, f"no reading dated {deadline.isoformat()}–{hi.isoformat()}"
    if cand is None:
        if as_of > hi + timedelta(days=rule.grace_days):
            return "void", None, f"no reading dated {deadline.isoformat()}–{hi.isoformat()} within the grace period"
        return "pending", None, "the deadline reading is not published yet"
    return "resolved", cand, ""


def resolve(call: Call, series: Series, as_of: date | None = None) -> Resolution:
    """Resolve one call against one series.

    ``as_of`` is the date the series copy was taken (defaults to ``series.as_of``,
    then to today). The function reads nothing else: same inputs, same answer.
    """
    if series.id != call.series_id:
        raise ValueError(f"{call.id}: resolves against {call.series_id!r}, given {series.id!r}")
    when = as_of or series.as_of or date.today()
    if when < call.deadline:
        return Resolution(status="pending", as_of=when, reason=f"deadline {call.deadline.isoformat()} not reached")
    status, reading, reason = select_reading(series, call.deadline, call.rule, when)
    if status != "resolved" or reading is None:
        return Resolution(
            status=status,
            as_of=when,
            reason=reason,
            reading_timestamp=reading[0] if reading and status == "pending" else None,
            reading_value=reading[1] if reading and status == "pending" else None,
        )
    t, v = reading
    tv = apply_transform(series, t, v, call.rule.transform)
    if tv is None:
        return Resolution(
            status="void",
            as_of=when,
            reason=f"no comparison reading {call.rule.transform.lag} before {t.isoformat()}",
            reading_timestamp=t,
            reading_value=v,
        )
    value, ct, cv = tv
    value = round(value, 9)
    outcome = call.rule.holds(value) if call.kind == "binary" else None
    return Resolution(
        status="resolved",
        as_of=when,
        reading_timestamp=t,
        reading_value=v,
        comparison_timestamp=ct,
        comparison_value=cv,
        value=value,
        outcome=outcome,
    )


def record(previous: Resolution | None, new: Resolution) -> Resolution:
    """Combine a stored resolution with a fresh one. The first resolution stands.

    - nothing stored, or stored but not resolved → the fresh one;
    - stored resolved, fresh resolved with a different value → stored, plus a
      ``revisions`` entry with the fresh value and date (the outcome does not change);
    - otherwise → stored.
    """
    if previous is None or not previous.resolved:
        return new
    if new.resolved and new.value is not None and previous.value is not None and abs(new.value - previous.value) > 1e-9:
        seen = {(r.get("as_of"), r.get("value")) for r in previous.revisions}
        key = (new.as_of.isoformat(), new.value)
        if key not in seen:
            rev = {"as_of": new.as_of.isoformat(), "value": new.value, "reading_value": new.reading_value}
            if new.outcome is not None and new.outcome != previous.outcome:
                rev["outcome_would_be"] = new.outcome
            return Resolution(**{**previous.__dict__, "revisions": previous.revisions + (rev,)})
    return previous


def resolve_all(calls: list[Call], series: dict[str, Series], as_of: date | None = None) -> list[Call]:
    """Resolve every call whose series is available, keeping earlier resolutions (see ``record``)."""
    out = []
    for c in calls:
        s = series.get(c.series_id)
        if s is None:
            out.append(c)
            continue
        out.append(c.with_resolution(record(c.resolution, resolve(c, s, as_of))))
    return out
