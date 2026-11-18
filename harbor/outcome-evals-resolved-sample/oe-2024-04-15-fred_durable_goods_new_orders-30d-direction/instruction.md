# Outcome Evals: oe-2024-04-15-fred_durable_goods_new_orders-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-fred_durable_goods_new_orders-30d-direction
Today is 2024-04-15.

Will the one-month change in U.S. durable goods new orders (Census M3, seasonally adjusted; computed from the level) for May 2024 (the latest monthly reading dated on or before 2024-05-15) be above 0.72%, its value for February 2024?

Resolves on the latest reading dated on or before 2024-05-15 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `fred_durable_goods_new_orders`. If no such reading is published within 103 days after the deadline, the question is void.
Series: Durable Goods · New Orders (U.S. Census Bureau), unit: USD m.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-03-01  277554  ->  0.187
2022-04-01  279157  ->  0.578
2022-05-01  278740  ->  -0.149
2022-06-01  284763  ->  2.161
2022-07-01  284460  ->  -0.106
2022-08-01  282368  ->  -0.735
2022-09-01  282430  ->  0.022
2022-10-01  287071  ->  1.643
2022-11-01  279095  ->  -2.778
2022-12-01  293358  ->  5.110
2023-01-01  288874  ->  -1.529
2023-02-01  280693  ->  -2.832
2023-03-01  289270  ->  3.056
2023-04-01  290168  ->  0.310
2023-05-01  289707  ->  -0.159
2023-06-01  303971  ->  4.924
2023-07-01  293278  ->  -3.518
2023-08-01  289128  ->  -1.415
2023-09-01  298229  ->  3.148
2023-10-01  285976  ->  -4.109
2023-11-01  298570  ->  4.404
2023-12-01  304324  ->  1.927
2024-01-01  280614  ->  -7.791
2024-02-01  282623  ->  0.716

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
