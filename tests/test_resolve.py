"""The resolver's written rules, one test (or more) per rule in resolve.py's docstring."""

from datetime import date

import pytest

from outcome_evals import Call, Resolution, Rule, Series, SeriesInfo, Transform, record, resolve
from outcome_evals.resolve import add_months, shift

D = date.fromisoformat


def monthly(values, start="2026-01-01", sid="s", ended_on=None):
    t = D(start)
    pairs = []
    for v in values:
        if v is not None:
            pairs.append((t, v))
        t = add_months(t, 1)
    return Series.from_pairs(SeriesInfo(id=sid, period="M", ended_on=ended_on), pairs)


def call(deadline="2026-06-18", made_on="2026-05-01", rule=None, kind="binary", sid="s"):
    return Call(
        id="q", question="Will it?", kind=kind, made_on=D(made_on), deadline=D(deadline), series_id=sid,
        rule=rule or Rule(comparator=">", threshold=4.0, period="M", grace_days=60), source="test", license="test",
    )


# 1. before the deadline
def test_pending_before_deadline():
    s = monthly([1, 2, 3, 4, 5, 6])
    r = resolve(call(deadline="2026-06-18"), s, as_of=D("2026-06-17"))
    assert r.status == "pending" and "not reached" in r.reason


# 2 + 3. the reading for the period containing the deadline is final when published
def test_last_on_or_before_final_by_cadence():
    s = monthly([1, 2, 3, 4, 5, 6])  # June reading dated 2026-06-01
    r = resolve(call(deadline="2026-06-18"), s, as_of=D("2026-07-15"))
    assert r.status == "resolved"
    assert r.reading_timestamp == D("2026-06-01") and r.value == 6 and r.outcome is True


def test_pending_while_a_closer_reading_may_come():
    # deadline 2026-07-02; only June is out; July (dated 07-01) would be closer and isn't published yet
    s = monthly([1, 2, 3, 4, 5, 6])
    r = resolve(call(deadline="2026-07-02"), s, as_of=D("2026-07-20"))
    assert r.status == "pending"


def test_final_once_a_later_reading_exists():
    s = Series.from_pairs(SeriesInfo(id="s", period="W"), [(D("2026-06-06"), 1.0), (D("2026-06-20"), 9.0)])
    # weekly series that skipped 06-13: deadline 06-14 picks 06-06 (within 8 days) once 06-20 exists
    rule = Rule(comparator=">", threshold=0.5, period="W")
    r = resolve(call(deadline="2026-06-14", rule=rule), s, as_of=D("2026-06-25"))
    assert r.status == "resolved" and r.reading_timestamp == D("2026-06-06")


# 4. missing reading on the deadline
def test_missing_reading_pending_then_void_after_grace():
    s = monthly([1, 2, 3, 4, 5])  # June never arrives
    c = call(deadline="2026-06-18")
    assert resolve(c, s, as_of=D("2026-07-20")).status == "pending"
    r = resolve(c, s, as_of=D("2026-08-18"))  # 61 days after the deadline, grace 60
    assert r.status == "void" and "within 60 days" in r.reason


def test_missing_reading_void_at_once_when_a_later_reading_exists():
    s = monthly([1, 2, 3, 4, 5, None, 7])  # June skipped, July published (Oct 2025 CPI case)
    r = resolve(call(deadline="2026-06-18"), s, as_of=D("2026-08-01"))
    assert r.status == "void" and "later reading exists" in r.reason


def test_after_grace_resolves_on_latest_in_window():
    # deadline 2026-07-02, July never published, June is within 31 days → after grace, June is used
    s = monthly([1, 2, 3, 4, 5, 6])
    r = resolve(call(deadline="2026-07-02"), s, as_of=D("2026-09-15"))
    assert r.status == "resolved" and r.reading_timestamp == D("2026-06-01")


def test_reading_too_old_is_not_used():
    s = monthly([1, 2, 3])  # last reading March; deadline June
    r = resolve(call(deadline="2026-06-18"), s, as_of=D("2026-12-01"))
    assert r.status == "void"


# 5. a series that ends
def test_series_that_ended_is_void():
    s = monthly([1, 2, 3], ended_on=D("2026-03-31"))
    r = resolve(call(deadline="2026-06-18"), s, as_of=D("2026-06-20"))
    assert r.status == "void" and "ended" in r.reason


# first_on_or_after
def test_first_on_or_after():
    s = Series.from_pairs(SeriesInfo(id="s", period="B"), [(D("2026-06-18"), 1.0), (D("2026-06-22"), 5.0)])
    rule = Rule(comparator=">", threshold=4.0, period="B", pick="first_on_or_after")
    r = resolve(call(deadline="2026-06-20", rule=rule), s, as_of=D("2026-06-23"))
    assert r.status == "resolved" and r.reading_timestamp == D("2026-06-22") and r.outcome is True
    r2 = resolve(call(deadline="2026-06-20", rule=rule), s.upto(D("2026-06-19")), as_of=D("2026-06-21"))
    assert r2.status == "pending"
    far = Series.from_pairs(SeriesInfo(id="s", period="B"), [(D("2026-07-30"), 5.0)])
    assert resolve(call(deadline="2026-06-20", rule=rule), far, as_of=D("2026-08-01")).status == "void"


# business days and weekends
def test_weekend_deadline_uses_friday_once_monday_due():
    s = Series.from_pairs(SeriesInfo(id="s", period="B"), [(D("2026-06-19"), 4.5)])  # Friday
    rule = Rule(comparator=">", threshold=4.0, period="B")
    # deadline Saturday: next business day (Monday) is after the deadline → Friday is final
    r = resolve(call(deadline="2026-06-20", rule=rule), s, as_of=D("2026-06-20"))
    assert r.status == "resolved" and r.reading_timestamp == D("2026-06-19")


# 6. transforms
def test_pct_change_12m():
    vals = [100.0 + i for i in range(18)]  # 2026-01 .. 2027-06
    s = monthly(vals, start="2026-01-01")
    rule = Rule(comparator=">", threshold=10.0, period="M", transform=Transform(kind="pct_change", lag="12M"))
    r = resolve(call(deadline="2027-03-15", made_on="2026-12-01", rule=rule), s, as_of=D("2027-06-30"))
    assert r.status == "resolved"
    assert r.reading_timestamp == D("2027-03-01") and r.comparison_timestamp == D("2026-03-01")
    assert r.value == pytest.approx((114 / 102 - 1) * 100)
    assert r.outcome is True


def test_change_and_annualized():
    s = monthly([10.0, 12.0, 15.0])
    rule = Rule(period="M", transform=Transform(kind="change", lag="1M"))
    r = resolve(call(deadline="2026-03-20", made_on="2026-02-01", rule=rule, kind="number"), s, as_of=D("2026-05-01"))
    assert r.value == 3.0 and r.outcome is None
    q = Series.from_pairs(SeriesInfo(id="s", period="Q"), [(D("2026-01-01"), 100.0), (D("2026-04-01"), 101.0)])
    rule = Rule(period="Q", transform=Transform(kind="annualized_pct_change", lag="1Q"))
    r = resolve(call(deadline="2026-05-01", made_on="2026-04-01", rule=rule, kind="number"), q, as_of=D("2026-09-01"))
    assert r.value == pytest.approx((1.01**4 - 1) * 100)


def test_missing_comparison_reading_is_void():
    s = monthly([100.0, None, 102.0, 103.0], start="2025-01-01")  # Feb 2025 missing
    s = s.merged(monthly([110.0, 111.0, 112.0], start="2026-01-01"))
    rule = Rule(comparator=">", threshold=0.0, period="M", transform=Transform(kind="pct_change", lag="12M"))
    r = resolve(call(deadline="2026-02-20", made_on="2026-01-15", rule=rule), s, as_of=D("2026-05-01"))
    assert r.status == "void" and "comparison" in r.reason


# 7. revisions
def test_first_resolution_stands_and_revision_is_logged():
    s1 = monthly([1, 2, 3, 4, 5, 6])
    s2 = monthly([1, 2, 3, 4, 5, 3.5])  # June revised below the threshold
    c = call(deadline="2026-06-18")
    first = resolve(c, s1, as_of=D("2026-07-15"))
    later = resolve(c, s2, as_of=D("2026-08-15"))
    kept = record(first, later)
    assert kept.outcome is True and kept.value == 6
    assert kept.revisions == ({"as_of": "2026-08-15", "value": 3.5, "reading_value": 3.5, "outcome_would_be": False},)
    assert record(kept, later) == kept  # recording the same revision twice adds nothing
    assert record(None, later) == later
    pending = Resolution(status="pending", as_of=D("2026-07-01"))
    assert record(pending, first) == first


def test_purity_same_inputs_same_answer():
    s = monthly([1, 2, 3, 4, 5, 6])
    c = call(deadline="2026-06-18")
    assert resolve(c, s, as_of=D("2026-07-15")) == resolve(c, s, as_of=D("2026-07-15"))


def test_wrong_series_raises():
    with pytest.raises(ValueError):
        resolve(call(sid="a"), monthly([1], sid="b"))


def test_between_is_half_open():
    r = Rule(comparator="between", low=1.0, high=2.0)
    assert r.holds(1.0) and r.holds(1.999) and not r.holds(2.0) and not r.holds(0.99)


def test_shift():
    assert shift(D("2026-01-31"), 1, "M") == D("2026-02-28")
    assert shift(D("2026-06-19"), 1, "B") == D("2026-06-22")
    assert shift(D("2026-06-22"), -1, "B") == D("2026-06-19")
    assert shift(D("2026-03-31"), -1, "Q") == D("2025-12-31")
