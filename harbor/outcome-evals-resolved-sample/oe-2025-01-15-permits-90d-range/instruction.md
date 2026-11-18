# Outcome Evals: oe-2025-01-15-permits-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-01-15-permits-90d-range
Today is 2025-01-15.

Will U.S. building permits for new private housing units (Census, seasonally adjusted annual rate, thousands) for April 2025 (the latest monthly reading dated on or before 2025-04-15) be at least 1,450 thousand and below 1,600 thousand?

Resolves on the latest reading dated on or before 2025-04-15 (and no more than 31 days before it), using the reading itself, as published in series `permits`. If no such reading is published within 95 days after the deadline, the question is void.
Series: New private housing units authorized (U.S. Census Bureau), unit: count.

Readings published by 2025-01-15 (latest 24, oldest first):
date  reading
2022-12-01  1398
2023-01-01  1418
2023-02-01  1605
2023-03-01  1472
2023-04-01  1482
2023-05-01  1579
2023-06-01  1447
2023-07-01  1530
2023-08-01  1596
2023-09-01  1530
2023-10-01  1524
2023-11-01  1513
2023-12-01  1501
2024-01-01  1548
2024-02-01  1570
2024-03-01  1477
2024-04-01  1456
2024-05-01  1405
2024-06-01  1459
2024-07-01  1448
2024-08-01  1492
2024-09-01  1421
2024-10-01  1435
2024-11-01  1512

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
