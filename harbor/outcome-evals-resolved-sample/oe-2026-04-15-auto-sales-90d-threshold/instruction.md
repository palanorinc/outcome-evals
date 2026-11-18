# Outcome Evals: oe-2026-04-15-auto-sales-90d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-auto-sales-90d-threshold
Today is 2026-04-15.

Will U.S. total light-vehicle sales (BEA, seasonally adjusted annual rate, millions of units) for July 2026 (the latest monthly reading dated on or before 2026-07-14) be above 17.25 million?

Resolves on the latest reading dated on or before 2026-07-14 (and no more than 31 days before it), using the reading itself, as published in series `auto-sales`. If no such reading is published within 83 days after the deadline, the question is void.
Series: Total light-vehicle sales (U.S. Bureau of Economic Analysis), unit: units.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading
2024-04-01  16.349
2024-05-01  16.427
2024-06-01  15.807
2024-07-01  16.187
2024-08-01  15.811
2024-09-01  16.306
2024-10-01  16.625
2024-11-01  17.025
2024-12-01  17.275
2025-01-01  16.317
2025-02-01  16.471
2025-03-01  18.189
2025-04-01  17.516
2025-05-01  16.158
2025-06-01  16.329
2025-07-01  16.843
2025-08-01  16.745
2025-09-01  16.961
2025-10-01  16.027
2025-11-01  16.154
2025-12-01  16.403
2026-01-01  15.357
2026-02-01  15.935
2026-03-01  16.449

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
