# Outcome Evals: oe-2024-10-15-rates.spread_2y10y-90d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-10-15-rates.spread_2y10y-90d-number
Today is 2024-10-15.

What will the 10-year minus 2-year U.S. Treasury par yield spread (Treasury daily par yield curve, percentage points) be for 2025-01-13 (or the last business day before it with a published reading)?

Resolves on the latest reading dated on or before 2025-01-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.spread_2y10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: Treasury Curve · 2s10s Spread (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pp.

Readings published by 2024-10-15 (latest 24, oldest first):
date  reading
2024-09-10  0.06
2024-09-11  0.03
2024-09-12  0.04
2024-09-13  0.09
2024-09-16  0.07
2024-09-17  0.06
2024-09-18  0.09
2024-09-19  0.14
2024-09-20  0.18
2024-09-23  0.18
2024-09-24  0.25
2024-09-25  0.26
2024-09-26  0.19
2024-09-27  0.2
2024-09-30  0.15
2024-10-01  0.13
2024-10-02  0.16
2024-10-03  0.15
2024-10-04  0.05
2024-10-07  0.04
2024-10-08  0.06
2024-10-09  0.07
2024-10-10  0.11
2024-10-11  0.13

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
