# Outcome Evals: oe-2025-10-15-fred_u6_underemployment-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-10-15-fred_u6_underemployment-90d-range
Today is 2025-10-15.

Will the U.S. U-6 underemployment rate (BLS, seasonally adjusted) for January 2026 (the latest monthly reading dated on or before 2026-01-13) be at least 7.6% and below 8.2%?

Resolves on the latest reading dated on or before 2026-01-13 (and no more than 31 days before it), using the reading itself, as published in series `fred_u6_underemployment`. If no such reading is published within 85 days after the deadline, the question is void.
Series: U-6 Underemployment Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2025-10-15 (latest 24, oldest first):
date  reading
2023-10-01  7.2
2023-11-01  7
2023-12-01  7.2
2024-01-01  7.2
2024-02-01  7.3
2024-03-01  7.3
2024-04-01  7.4
2024-05-01  7.4
2024-06-01  7.4
2024-07-01  7.8
2024-08-01  7.8
2024-09-01  7.7
2024-10-01  7.7
2024-11-01  7.7
2024-12-01  7.6
2025-01-01  7.5
2025-02-01  8
2025-03-01  7.9
2025-04-01  7.8
2025-05-01  7.8
2025-06-01  7.7
2025-07-01  7.9
2025-08-01  8.1
2025-09-01  8.1

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
