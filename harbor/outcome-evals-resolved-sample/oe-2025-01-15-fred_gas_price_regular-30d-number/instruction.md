# Outcome Evals: oe-2025-01-15-fred_gas_price_regular-30d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-01-15-fred_gas_price_regular-30d-number
Today is 2025-01-15.

What will the U.S. average retail price of regular gasoline (EIA weekly survey, dollars a gallon) be for the latest weekly reading dated on or before 2025-02-14 (expected: 2025-02-10)?

Resolves on the latest reading dated on or before 2025-02-14 (and no more than 8 days before it), using the reading itself, as published in series `fred_gas_price_regular`. If no such reading is published within 47 days after the deadline, the question is void.
Series: US Regular Gasoline Price (Weekly) (U.S. Energy Information Administration), unit: $/gal.

Readings published by 2025-01-15 (latest 24, oldest first):
date  reading
2024-08-05  3.448
2024-08-12  3.414
2024-08-19  3.382
2024-08-26  3.313
2024-09-02  3.289
2024-09-09  3.236
2024-09-16  3.18
2024-09-23  3.185
2024-09-30  3.179
2024-10-07  3.136
2024-10-14  3.171
2024-10-21  3.144
2024-10-28  3.097
2024-11-04  3.069
2024-11-11  3.052
2024-11-18  3.046
2024-11-25  3.044
2024-12-02  3.034
2024-12-09  3.008
2024-12-16  3.016
2024-12-23  3.024
2024-12-30  3.006
2025-01-06  3.047
2025-01-13  3.043

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
