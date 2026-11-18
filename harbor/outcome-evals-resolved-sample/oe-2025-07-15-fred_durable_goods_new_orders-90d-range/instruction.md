# Outcome Evals: oe-2025-07-15-fred_durable_goods_new_orders-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-fred_durable_goods_new_orders-90d-range
Today is 2025-07-15.

Will the one-month change in U.S. durable goods new orders (Census M3, seasonally adjusted; computed from the level) for October 2025 (the latest monthly reading dated on or before 2025-10-13) be at least 13.50% and below 19.50%?

Resolves on the latest reading dated on or before 2025-10-13 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `fred_durable_goods_new_orders`. If no such reading is published within 103 days after the deadline, the question is void.
Series: Durable Goods · New Orders (U.S. Census Bureau), unit: USD m.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-06-01  303971  ->  4.924
2023-07-01  293278  ->  -3.518
2023-08-01  289128  ->  -1.415
2023-09-01  298229  ->  3.148
2023-10-01  285976  ->  -4.109
2023-11-01  298570  ->  4.404
2023-12-01  304324  ->  1.927
2024-01-01  280614  ->  -7.791
2024-02-01  282623  ->  0.716
2024-03-01  287423  ->  1.698
2024-04-01  286972  ->  -0.157
2024-05-01  286829  ->  -0.050
2024-06-01  281128  ->  -1.988
2024-07-01  293234  ->  4.306
2024-08-01  289926  ->  -1.128
2024-09-01  292469  ->  0.877
2024-10-01  293266  ->  0.273
2024-11-01  288340  ->  -1.680
2024-12-01  290559  ->  0.770
2025-01-01  291195  ->  0.219
2025-02-01  293985  ->  0.958
2025-03-01  316215  ->  7.562
2025-04-01  295229  ->  -6.637
2025-05-01  344069  ->  16.543

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
