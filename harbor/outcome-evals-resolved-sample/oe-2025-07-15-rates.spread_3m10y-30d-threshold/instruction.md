# Outcome Evals: oe-2025-07-15-rates.spread_3m10y-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-rates.spread_3m10y-30d-threshold
Today is 2025-07-15.

Will the 10-year minus 3-month U.S. Treasury par yield spread (Treasury daily par yield curve, percentage points) for 2025-08-14 (or the last business day before it with a published reading) be above 0.15 pp?

Resolves on the latest reading dated on or before 2025-08-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.spread_3m10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: Treasury Curve · 3m10y Spread (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pp.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading
2025-06-09  0.05
2025-06-10  0.02
2025-06-11  -0.04
2025-06-12  -0.1
2025-06-13  -0.04
2025-06-16  0.03
2025-06-17  -0.03
2025-06-18  -0.04
2025-06-20  -0.01
2025-06-23  -0.04
2025-06-24  -0.08
2025-06-25  -0.09
2025-06-26  -0.13
2025-06-27  -0.1
2025-06-30  -0.17
2025-07-01  -0.14
2025-07-02  -0.11
2025-07-03  -0.07
2025-07-07  -0.02
2025-07-08  0
2025-07-09  -0.08
2025-07-10  -0.07
2025-07-11  0.02
2025-07-14  0.01

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
