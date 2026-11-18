# Outcome Evals: oe-2026-07-15-rates.spread_2y10y-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-07-15-rates.spread_2y10y-90d-direction
Today is 2026-07-15.

Will the 10-year minus 2-year U.S. Treasury par yield spread (Treasury daily par yield curve, percentage points) for 2026-10-13 (or the last business day before it with a published reading) be above 0.40 pp, its value for 2026-07-14?

Resolves on the latest reading dated on or before 2026-10-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.spread_2y10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: Treasury Curve · 2s10s Spread (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pp.

Readings published by 2026-07-15 (latest 24, oldest first):
date  reading
2026-06-09  0.4
2026-06-10  0.42
2026-06-11  0.4
2026-06-12  0.39
2026-06-15  0.4
2026-06-16  0.38
2026-06-17  0.29
2026-06-18  0.27
2026-06-22  0.27
2026-06-23  0.34
2026-06-24  0.3
2026-06-25  0.31
2026-06-26  0.31
2026-06-29  0.28
2026-06-30  0.3
2026-07-01  0.31
2026-07-02  0.35
2026-07-06  0.35
2026-07-07  0.36
2026-07-08  0.35
2026-07-09  0.38
2026-07-10  0.35
2026-07-13  0.36
2026-07-14  0.4

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
