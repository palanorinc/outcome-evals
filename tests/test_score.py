import math
from datetime import date

import pytest

from outcome_evals import Anchor, Call, Forecast, Resolution, Rule, UnresolvedCallError, score_call, summarize
from outcome_evals.score import brier, calibration, hit, log_score, pinball

D = date.fromisoformat


def c(i, p=None, outcome=None, status="resolved", kind="binary", value=None, anchor=4.0, base_rate=0.4, fc_value=None, scale=None, base_change=None):
    rule = Rule(comparator=">", threshold=4.5) if kind == "binary" else Rule()
    res = None
    if status:
        v = value if value is not None else (5.0 if outcome else 4.0)
        res = Resolution(status=status, as_of=D("2026-12-01"), value=v if status == "resolved" else None,
                         outcome=outcome if (status == "resolved" and kind == "binary") else None)
    fc = None
    if p is not None:
        fc = Forecast(probability=p)
    if fc_value is not None:
        fc = Forecast(value=fc_value)
    return Call(
        id=f"q{i}", question="?", kind=kind, made_on=D("2026-01-01"), deadline=D("2026-02-01"), series_id="s", rule=rule,
        source="t", license="t", anchor=Anchor(D("2025-12-01"), anchor), base_rate=base_rate if kind == "binary" else None,
        forecast=fc, resolution=res, scale=scale, base_change=base_change,
    )


def test_brier_log_hit():
    assert brier(0.7, True) == pytest.approx(0.09)
    assert brier(0.7, False) == pytest.approx(0.49)
    assert log_score(0.7, True) == pytest.approx(math.log(0.7))
    assert log_score(0.0, True) == pytest.approx(math.log(1e-4))  # clipped, not -inf
    assert hit(0.5, True) == 0.5 and hit(0.6, True) == 1.0 and hit(0.6, False) == 0.0


def test_never_scores_unresolved():
    with pytest.raises(UnresolvedCallError):
        score_call(c(1, p=0.6, status="pending"))
    with pytest.raises(UnresolvedCallError):
        score_call(c(1, p=0.6, status="void"))
    with pytest.raises(UnresolvedCallError):
        score_call(c(1, p=0.6, status=None))


def test_summarize_counts_but_never_scores_unresolved():
    calls = [
        c(1, p=0.8, outcome=True),
        c(2, p=0.3, outcome=False),
        c(3, p=0.9, status="pending"),
        c(4, p=0.9, status="void"),
        c(5, outcome=True),  # resolved, no forecast
    ]
    s = summarize(calls)
    assert (s.n_calls, s.n_resolved, s.n_pending, s.n_void, s.n_unforecast) == (5, 3, 1, 1, 1)
    assert s.binary["n"] == 2
    assert s.binary["forecast"]["brier"] == pytest.approx((0.04 + 0.09) / 2)
    assert s.binary["forecast"]["hit_rate"] == 1.0
    # no change: anchor 4.0 is not > 4.5 → p = 0; outcomes yes, no → Brier (1 + 0) / 2
    assert s.binary["no_change"]["brier"] == pytest.approx(0.5)
    assert s.binary["no_change"]["hit_rate"] == pytest.approx(0.5)
    # base rate 0.4 → (0.36 + 0.16) / 2
    assert s.binary["base_rate"]["brier"] == pytest.approx(0.26)
    assert {x.id for x in s.scores} == {"q1", "q2"}
    assert "pending: 1" in s.text()


def test_calibration_bins():
    bins = calibration([(0.05, False), (0.15, True), (0.95, True), (1.0, True), (0.91, False)])
    top = bins[-1]
    assert top.n == 3 and top.mean_probability == pytest.approx((0.95 + 1.0 + 0.91) / 3) and top.observed_frequency == pytest.approx(2 / 3)
    assert bins[0].n == 1 and bins[1].n == 1 and sum(b.n for b in bins) == 5


def test_number_scores_and_skill():
    calls = [
        c(1, kind="number", value=5.0, fc_value=4.5, anchor=4.0, scale=0.5, base_change=0.2),
        c(2, kind="number", value=3.0, fc_value=3.5, anchor=4.0, scale=0.5, base_change=0.2),
    ]
    s = summarize(calls)
    f = s.number["forecast"]
    assert f["mean_abs_error"] == pytest.approx(0.5)
    assert f["mean_scaled_abs_error"] == pytest.approx(1.0)
    assert s.number["no_change"]["mean_scaled_abs_error"] == pytest.approx(2.0)
    assert f["skill_vs_no_change"] == pytest.approx(0.5)
    # base rate baseline: anchor + base_change = 4.2 → errors 0.8 and 1.2, scaled by 0.5
    assert s.number["base_rate"]["mean_scaled_abs_error"] == pytest.approx(2.0)


def test_quantile_forecast():
    assert pinball([0.1, 0.5, 0.9], [1.0, 2.0, 3.0], 2.0) == pytest.approx((0.1 * 1 + 0 + 0.1 * 1) / 3)
    call = c(1, kind="number", value=2.0)
    cs = score_call(call, Forecast(quantile_levels=(0.1, 0.5, 0.9), quantiles=(1.0, 2.5, 3.0)))
    assert cs.forecast_value == 2.5 and cs.abs_error == pytest.approx(0.5) and cs.quantile_loss is not None
