# Outcome Evals: oe-2025-01-15-auto-sales-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-01-15-auto-sales-90d-range
Today is 2025-01-15.

Will U.S. total light-vehicle sales (BEA, seasonally adjusted annual rate, millions of units) for April 2025 (the latest monthly reading dated on or before 2025-04-15) be at least 16.75 million and below 18.00 million?

Resolves on the latest reading dated on or before 2025-04-15 (and no more than 31 days before it), using the reading itself, as published in series `auto-sales`. If no such reading is published within 83 days after the deadline, the question is void.
Series: Total light-vehicle sales (U.S. Bureau of Economic Analysis), unit: units.

Readings published by 2025-01-15 (latest 24, oldest first):
date  reading
2023-01-01  15.93
2023-02-01  15.48
2023-03-01  15.491
2023-04-01  16.345
2023-05-01  15.978
2023-06-01  16.592
2023-07-01  16.206
2023-08-01  15.916
2023-09-01  16.185
2023-10-01  15.844
2023-11-01  15.864
2023-12-01  16.308
2024-01-01  15.862
2024-02-01  16.259
2024-03-01  16.064
2024-04-01  16.349
2024-05-01  16.427
2024-06-01  15.807
2024-07-01  16.187
2024-08-01  15.811
2024-09-01  16.306
2024-10-01  16.625
2024-11-01  17.025
2024-12-01  17.275

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
