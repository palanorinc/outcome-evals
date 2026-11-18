"""Score a fictional company's private calls end to end.

Bramblewick Hardware Co. is made up. Its planning team wrote down ten dated
calls in 2025 and 2026: eight about public U.S. series, two about its own
weekly online orders (a synthetic series in this folder). This script resolves
each call against the series, adds the two baselines, and prints the scores.

    python examples/bring_your_own_calls/run.py
    PALANOR_API_KEY=... python examples/bring_your_own_calls/run.py --api   # public series from Palanor's API
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from outcome_evals import LocalData, PalanorAPI, Series, SeriesInfo, load_calls, resolve_all, summarize, with_baselines

HERE = Path(__file__).resolve().parent


def main() -> None:
    calls = load_calls(HERE / "bramblewick_calls.jsonl")

    # Public series: the files shipped with the package (no key), or Palanor's API.
    public_ids = sorted({c.series_id for c in calls if not c.series_id.startswith("bramblewick.")})
    if "--api" in sys.argv:
        series = PalanorAPI().many(public_ids)
        as_of = date.today()
    else:
        local = LocalData()
        series = {i: local.series(i) for i in public_ids}
        as_of = date.fromisoformat(local.manifest()["as_of"])

    # The company's own series: any CSV with timestamp and target columns.
    own = Series.from_csv(
        (HERE / "bramblewick_weekly_orders.csv").read_text(),
        SeriesInfo(id="bramblewick.weekly_orders", name="Weekly online orders", period="W", publish_lag_days=2),
    )
    series[own.id] = own

    # Baselines from what was known on each call's date, then resolve.
    calls = [with_baselines(c, series[c.series_id]) for c in calls]
    calls = resolve_all(calls, series, as_of=as_of)

    print(f"Bramblewick Hardware Co. (fictional): {len(calls)} calls, series as of {as_of.isoformat()}\n")
    for c in calls:
        r = c.resolution
        assert r is not None
        if c.kind == "binary":
            said = f"said {c.forecast.probability:.0%}" if c.forecast and c.forecast.probability is not None else ""
            got = {"resolved": "yes" if r.outcome else "no", "pending": "open", "void": "void"}[r.status]
        else:
            said = f"said {c.forecast.value:g}" if c.forecast and c.forecast.value is not None else ""
            got = f"{r.value:g}" if r.value is not None else r.status
        when = f" ({r.reading_timestamp.isoformat()})" if r.reading_timestamp and r.status == "resolved" else ""
        print(f"  {c.id}  {said:<10} → {got}{when}  {c.question}")
    print()
    print(summarize(calls).text())


if __name__ == "__main__":
    main()
