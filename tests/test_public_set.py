"""Checks on the shipped question set: licences, labels, and no look-ahead."""

from datetime import date, timedelta
from pathlib import Path

import pytest

from outcome_evals import LocalData, Series, resolve
from outcome_evals.baselines import history
from outcome_evals.public_set import SPEC_BY_ID, SPECS, generate

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SOURCES = {"bls", "bea", "us_census", "us_dol", "us_treasury", "eia"}


@pytest.fixture(scope="module")
def data():
    return LocalData()


def test_every_series_is_public_domain_and_credited(data):
    man = data.manifest()
    assert man["series"], "no series shipped"
    licences = (ROOT / "DATA-LICENSES.md").read_text()
    for e in man["series"]:
        assert e["license_class"] == "public_domain", e["id"]
        assert e["source"] in ALLOWED_SOURCES, e["id"]
        assert e["attribution"] and e["license_url"].startswith("https://"), e["id"]
        assert f"`{e['source']}`" in licences, f"{e['source']} not quoted in DATA-LICENSES.md"
        assert f"`{e['id']}`" in licences, f"{e['id']} not listed in DATA-LICENSES.md"
    assert {s.id for s in SPECS} == {e["id"] for e in man["series"]}


def test_no_prediction_market_vintage_or_single_security_series():
    for s in SPECS:
        low = (s.id + " " + s.noun + " " + s.agency_series).lower()
        for banned in ("kalshi", "polymarket", "manifold", "alfred", "vintage", "stock", "share price", "equity"):
            assert banned not in low, (s.id, banned)


def test_ids_unique_and_splits_labelled(data):
    hist = data.questions("resolved_history")
    live = data.questions("live")
    ids = [c.id for c in hist + live]
    assert len(ids) == len(set(ids))
    assert hist and all(c.split == "resolved_history" for c in hist)
    assert live and all(c.split == "live" for c in live)
    assert all(c.resolution is not None and c.resolution.resolved for c in hist)


def test_history_has_no_look_ahead(data):
    for c in data.questions("resolved_history"):
        lag = SPEC_BY_ID[c.series_id].publish_lag_days
        assert c.cutoff is not None and c.cutoff <= c.made_on - timedelta(days=lag), c.id
        assert c.anchor is not None and c.anchor.timestamp <= c.cutoff, c.id


def test_live_questions_are_open_on_the_day_they_are_made(data):
    series = data.all_series()
    for c in data.questions("live"):
        assert c.cutoff is not None and c.cutoff <= c.made_on
        assert c.horizon_days in (30, 90)
        r = resolve(c, series[c.series_id], as_of=c.made_on)
        assert r.status == "pending", c.id
        # the reading the question is about is dated after anything known on made_on
        assert c.deadline > c.made_on


def test_baselines_ignore_everything_after_the_cutoff(data):
    s = data.series("fred_unemployment")
    cutoff, deadline = date(2024, 6, 1), date(2024, 8, 15)
    spec = SPEC_BY_ID["fred_unemployment"]
    rule = spec.rule(comparator=">", threshold=4.0)
    h1 = history(s, cutoff, deadline, rule)
    # rewrite every later reading wildly: nothing may change
    later = [(t, v * 10) for t, v in s.pairs() if t > cutoff]
    s2 = Series.from_pairs(s.info, [p for p in s.pairs() if p[0] <= cutoff] + later)
    h2 = history(s2, cutoff, deadline, rule)
    assert h1 is not None and h2 is not None
    assert h1.changes == h2.changes and h1.anchor == h2.anchor
    assert h1.base_rate(rule) == h2.base_rate(rule)


def test_generation_is_deterministic(data):
    series = data.all_series()
    a = generate(series, date(2025, 3, 15), "resolved_history")
    b = generate(series, date(2025, 3, 15), "resolved_history")
    assert [x.to_dict() for x in a] == [x.to_dict() for x in b]


def test_history_caveat_in_readme():
    text = (ROOT / "README.md").read_text()
    assert "not a test of forecasting for any model trained after the outcome" in text
