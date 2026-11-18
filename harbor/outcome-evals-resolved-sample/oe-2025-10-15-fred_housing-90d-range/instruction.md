# Outcome Evals: oe-2025-10-15-fred_housing-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-10-15-fred_housing-90d-range
Today is 2025-10-15.

Will U.S. housing starts (Census, seasonally adjusted annual rate, thousands of units) for January 2026 (the latest monthly reading dated on or before 2026-01-13) be at least 1,225 thousand and below 1,400 thousand?

Resolves on the latest reading dated on or before 2026-01-13 (and no more than 31 days before it), using the reading itself, as published in series `fred_housing`. If no such reading is published within 95 days after the deadline, the question is void.
Series: Housing Starts (U.S. Census Bureau), unit: count.

Readings published by 2025-10-15 (latest 24, oldest first):
date  reading
2023-09-01  1369
2023-10-01  1380
2023-11-01  1522
2023-12-01  1504
2024-01-01  1378
2024-02-01  1555
2024-03-01  1297
2024-04-01  1379
2024-05-01  1329
2024-06-01  1318
2024-07-01  1269
2024-08-01  1394
2024-09-01  1357
2024-10-01  1370
2024-11-01  1300
2024-12-01  1494
2025-01-01  1353
2025-02-01  1491
2025-03-01  1346
2025-04-01  1400
2025-05-01  1289
2025-06-01  1379
2025-07-01  1432
2025-08-01  1291

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
