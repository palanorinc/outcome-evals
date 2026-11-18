# Outcome Evals: oe-2026-01-15-fred_savings_rate-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-01-15-fred_savings_rate-90d-direction
Today is 2026-01-15.

Will the U.S. personal saving rate (BEA, seasonally adjusted) for April 2026 (the latest monthly reading dated on or before 2026-04-15) be above 4.9%, its value for November 2025?

Resolves on the latest reading dated on or before 2026-04-15 (and no more than 31 days before it), using the reading itself, as published in series `fred_savings_rate`. If no such reading is published within 107 days after the deadline, the question is void.
Series: Personal Savings Rate (U.S. Bureau of Economic Analysis), unit: %.

Readings published by 2026-01-15 (latest 24, oldest first):
date  reading
2023-12-01  6.6
2024-01-01  7.2
2024-02-01  6.9
2024-03-01  6.7
2024-04-01  6.7
2024-05-01  6.6
2024-06-01  6.6
2024-07-01  6.2
2024-08-01  6.2
2024-09-01  5.7
2024-10-01  5.8
2024-11-01  5.7
2024-12-01  5.1
2025-01-01  5.7
2025-02-01  5.7
2025-03-01  5.7
2025-04-01  6.2
2025-05-01  5.7
2025-06-01  5.5
2025-07-01  5.3
2025-08-01  5.2
2025-09-01  5.1
2025-10-01  4.9
2025-11-01  4.9

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
