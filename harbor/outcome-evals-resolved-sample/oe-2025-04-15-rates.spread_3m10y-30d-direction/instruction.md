# Outcome Evals: oe-2025-04-15-rates.spread_3m10y-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-rates.spread_3m10y-30d-direction
Today is 2025-04-15.

Will the 10-year minus 3-month U.S. Treasury par yield spread (Treasury daily par yield curve, percentage points) for 2025-05-15 (or the last business day before it with a published reading) be above 0.05 pp, its value for 2025-04-14?

Resolves on the latest reading dated on or before 2025-05-15 (and no more than 5 days before it), using the reading itself, as published in series `rates.spread_3m10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: Treasury Curve · 3m10y Spread (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pp.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2025-03-12  -0.03
2025-03-13  -0.07
2025-03-14  -0.02
2025-03-17  -0.03
2025-03-18  -0.05
2025-03-19  -0.08
2025-03-20  -0.09
2025-03-21  -0.08
2025-03-24  0.01
2025-03-25  -0.02
2025-03-26  0.02
2025-03-27  0.05
2025-03-28  -0.06
2025-03-31  -0.09
2025-04-01  -0.15
2025-04-02  -0.12
2025-04-03  -0.25
2025-04-04  -0.27
2025-04-07  -0.14
2025-04-08  -0.05
2025-04-09  -0.01
2025-04-10  0.06
2025-04-11  0.14
2025-04-14  0.05

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
