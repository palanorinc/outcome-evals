# Outcome Evals: oe-2026-01-15-construction-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-01-15-construction-30d-threshold
Today is 2026-01-15.

Will the one-month change in U.S. total construction spending (Census, seasonally adjusted annual rate; computed from the level) for February 2026 (the latest monthly reading dated on or before 2026-02-14) be above -0.30%?

Resolves on the latest reading dated on or before 2026-02-14 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `construction`. If no such reading is published within 108 days after the deadline, the question is void.
Series: Total construction spending (U.S. Census Bureau), unit: $bn.

Readings published by 2026-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-12-01  2.17485e+06  ->  0.208
2024-01-01  2.19163e+06  ->  0.772
2024-02-01  2.22092e+06  ->  1.337
2024-03-01  2.21411e+06  ->  -0.307
2024-04-01  2.22069e+06  ->  0.297
2024-05-01  2.23284e+06  ->  0.547
2024-06-01  2.23864e+06  ->  0.260
2024-07-01  2.24044e+06  ->  0.080
2024-08-01  2.24598e+06  ->  0.247
2024-09-01  2.2631e+06  ->  0.762
2024-10-01  2.26382e+06  ->  0.032
2024-11-01  2.26264e+06  ->  -0.052
2024-12-01  2.25882e+06  ->  -0.169
2025-01-01  2.26105e+06  ->  0.099
2025-02-01  2.26581e+06  ->  0.210
2025-03-01  2.25626e+06  ->  -0.422
2025-04-01  2.26381e+06  ->  0.335
2025-05-01  2.24443e+06  ->  -0.856
2025-06-01  2.23772e+06  ->  -0.299
2025-07-01  2.24263e+06  ->  0.220
2025-08-01  2.24202e+06  ->  -0.027
2025-09-01  2.2458e+06  ->  0.168
2025-10-01  2.24114e+06  ->  -0.207
2025-11-01  2.22073e+06  ->  -0.911

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
