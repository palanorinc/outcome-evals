# Outcome Evals: oe-2026-07-15-fred_unemployment-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-07-15-fred_unemployment-90d-range
Today is 2026-07-15.

Will the U.S. unemployment rate (BLS, seasonally adjusted) for October 2026 (the latest monthly reading dated on or before 2026-10-13) be at least 3.9% and below 4.3%?

Resolves on the latest reading dated on or before 2026-10-13 (and no more than 31 days before it), using the reading itself, as published in series `fred_unemployment`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Unemployment Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2026-07-15 (latest 24, oldest first):
date  reading
2024-06-01  4.1
2024-07-01  4.2
2024-08-01  4.2
2024-09-01  4.1
2024-10-01  4.1
2024-11-01  4.2
2024-12-01  4.1
2025-01-01  4
2025-02-01  4.2
2025-03-01  4.2
2025-04-01  4.2
2025-05-01  4.3
2025-06-01  4.1
2025-07-01  4.3
2025-08-01  4.3
2025-09-01  4.4
2025-11-01  4.5
2025-12-01  4.4
2026-01-01  4.3
2026-02-01  4.4
2026-03-01  4.3
2026-04-01  4.3
2026-05-01  4.3
2026-06-01  4.2

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
