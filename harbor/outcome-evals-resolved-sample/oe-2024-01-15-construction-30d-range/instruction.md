# Outcome Evals: oe-2024-01-15-construction-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-construction-30d-range
Today is 2024-01-15.

Will the one-month change in U.S. total construction spending (Census, seasonally adjusted annual rate; computed from the level) for February 2024 (the latest monthly reading dated on or before 2024-02-14) be at least 0.70% and below 2.10%?

Resolves on the latest reading dated on or before 2024-02-14 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `construction`. If no such reading is published within 108 days after the deadline, the question is void.
Series: Total construction spending (U.S. Census Bureau), unit: $bn.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2021-12-01  1.76235e+06  ->  1.760
2022-01-01  1.80776e+06  ->  2.577
2022-02-01  1.84207e+06  ->  1.898
2022-03-01  1.8774e+06  ->  1.918
2022-04-01  1.91315e+06  ->  1.904
2022-05-01  1.92396e+06  ->  0.565
2022-06-01  1.92027e+06  ->  -0.192
2022-07-01  1.92386e+06  ->  0.187
2022-08-01  1.91806e+06  ->  -0.301
2022-09-01  1.91789e+06  ->  -0.009
2022-10-01  1.91437e+06  ->  -0.184
2022-11-01  1.91954e+06  ->  0.270
2022-12-01  1.92688e+06  ->  0.382
2023-01-01  1.95762e+06  ->  1.595
2023-02-01  1.97118e+06  ->  0.693
2023-03-01  2.00043e+06  ->  1.484
2023-04-01  2.02892e+06  ->  1.424
2023-05-01  2.0539e+06  ->  1.231
2023-06-01  2.07423e+06  ->  0.990
2023-07-01  2.08362e+06  ->  0.452
2023-08-01  2.10845e+06  ->  1.192
2023-09-01  2.11718e+06  ->  0.414
2023-10-01  2.13959e+06  ->  1.059
2023-11-01  2.17032e+06  ->  1.436

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
