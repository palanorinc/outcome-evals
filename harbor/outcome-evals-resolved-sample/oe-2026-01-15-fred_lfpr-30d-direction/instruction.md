# Outcome Evals: oe-2026-01-15-fred_lfpr-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-01-15-fred_lfpr-30d-direction
Today is 2026-01-15.

Will the U.S. labor force participation rate (BLS, seasonally adjusted) for February 2026 (the latest monthly reading dated on or before 2026-02-14) be above 62.4%, its value for December 2025?

Resolves on the latest reading dated on or before 2026-02-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_lfpr`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Labor Force Participation Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2026-01-15 (latest 24, oldest first):
date  reading
2023-12-01  62.5
2024-01-01  62.5
2024-02-01  62.6
2024-03-01  62.7
2024-04-01  62.6
2024-05-01  62.6
2024-06-01  62.6
2024-07-01  62.7
2024-08-01  62.7
2024-09-01  62.7
2024-10-01  62.5
2024-11-01  62.4
2024-12-01  62.5
2025-01-01  62.6
2025-02-01  62.5
2025-03-01  62.5
2025-04-01  62.6
2025-05-01  62.4
2025-06-01  62.3
2025-07-01  62.2
2025-08-01  62.3
2025-09-01  62.5
2025-11-01  62.5
2025-12-01  62.4

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
