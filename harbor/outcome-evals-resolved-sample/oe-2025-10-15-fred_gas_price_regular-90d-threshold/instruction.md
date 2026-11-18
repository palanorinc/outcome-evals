# Outcome Evals: oe-2025-10-15-fred_gas_price_regular-90d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-10-15-fred_gas_price_regular-90d-threshold
Today is 2025-10-15.

Will the U.S. average retail price of regular gasoline (EIA weekly survey, dollars a gallon) for the latest weekly reading dated on or before 2026-01-13 (expected: 2026-01-12) be above $3.300?

Resolves on the latest reading dated on or before 2026-01-13 (and no more than 8 days before it), using the reading itself, as published in series `fred_gas_price_regular`. If no such reading is published within 47 days after the deadline, the question is void.
Series: US Regular Gasoline Price (Weekly) (U.S. Energy Information Administration), unit: $/gal.

Readings published by 2025-10-15 (latest 24, oldest first):
date  reading
2025-05-05  3.147
2025-05-12  3.12
2025-05-19  3.173
2025-05-26  3.16
2025-06-02  3.127
2025-06-09  3.108
2025-06-16  3.139
2025-06-23  3.213
2025-06-30  3.164
2025-07-07  3.125
2025-07-14  3.13
2025-07-21  3.121
2025-07-28  3.123
2025-08-04  3.14
2025-08-11  3.118
2025-08-18  3.125
2025-08-25  3.147
2025-09-01  3.177
2025-09-08  3.192
2025-09-15  3.168
2025-09-22  3.173
2025-09-29  3.118
2025-10-06  3.124
2025-10-13  3.061

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
