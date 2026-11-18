# Outcome Evals: oe-2025-04-15-fred_housing-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-fred_housing-90d-direction
Today is 2025-04-15.

Will U.S. housing starts (Census, seasonally adjusted annual rate, thousands of units) for July 2025 (the latest monthly reading dated on or before 2025-07-14) be above 1,491 thousand, its value for February 2025?

Resolves on the latest reading dated on or before 2025-07-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_housing`. If no such reading is published within 95 days after the deadline, the question is void.
Series: Housing Starts (U.S. Census Bureau), unit: count.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2023-03-01  1366
2023-04-01  1343
2023-05-01  1609
2023-06-01  1420
2023-07-01  1464
2023-08-01  1321
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
