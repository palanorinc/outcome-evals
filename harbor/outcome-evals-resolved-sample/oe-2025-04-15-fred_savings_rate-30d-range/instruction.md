# Outcome Evals: oe-2025-04-15-fred_savings_rate-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-fred_savings_rate-30d-range
Today is 2025-04-15.

Will the U.S. personal saving rate (BEA, seasonally adjusted) for May 2025 (the latest monthly reading dated on or before 2025-05-15) be at least 5.0% and below 6.2%?

Resolves on the latest reading dated on or before 2025-05-15 (and no more than 31 days before it), using the reading itself, as published in series `fred_savings_rate`. If no such reading is published within 107 days after the deadline, the question is void.
Series: Personal Savings Rate (U.S. Bureau of Economic Analysis), unit: %.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2023-03-01  6.1
2023-04-01  6.1
2023-05-01  6.4
2023-06-01  6.3
2023-07-01  6.2
2023-08-01  6.3
2023-09-01  6
2023-10-01  6.2
2023-11-01  6.4
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
