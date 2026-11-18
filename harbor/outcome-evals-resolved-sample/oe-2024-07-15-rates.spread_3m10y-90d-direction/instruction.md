# Outcome Evals: oe-2024-07-15-rates.spread_3m10y-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-rates.spread_3m10y-90d-direction
Today is 2024-07-15.

Will the 10-year minus 3-month U.S. Treasury par yield spread (Treasury daily par yield curve, percentage points) for 2024-10-13 (or the last business day before it with a published reading) be above -1.25 pp, its value for 2024-07-12?

Resolves on the latest reading dated on or before 2024-10-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.spread_3m10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: Treasury Curve · 3m10y Spread (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pp.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading
2024-06-07  -1.09
2024-06-10  -1.05
2024-06-11  -1.13
2024-06-12  -1.2
2024-06-13  -1.27
2024-06-14  -1.31
2024-06-17  -1.24
2024-06-18  -1.28
2024-06-20  -1.25
2024-06-21  -1.24
2024-06-24  -1.25
2024-06-25  -1.26
2024-06-26  -1.18
2024-06-27  -1.2
2024-06-28  -1.12
2024-07-01  -0.99
2024-07-02  -1.04
2024-07-03  -1.11
2024-07-05  -1.18
2024-07-08  -1.18
2024-07-09  -1.16
2024-07-10  -1.18
2024-07-11  -1.24
2024-07-12  -1.25

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
