# Outcome Evals: oe-2024-01-15-retail-sales-90d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-retail-sales-90d-number
Today is 2024-01-15.

What will the one-month change in U.S. advance retail and food services sales (Census, seasonally adjusted; computed from the level) be for April 2024 (the latest monthly reading dated on or before 2024-04-14)?

Resolves on the latest reading dated on or before 2024-04-14 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `retail-sales`. If no such reading is published within 92 days after the deadline, the question is void.
Series: Retail sales · advance (U.S. Census Bureau), unit: index.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2021-12-01  621734  ->  -0.678
2022-01-01  634120  ->  1.992
2022-02-01  640815  ->  1.056
2022-03-01  652673  ->  1.850
2022-04-01  661508  ->  1.354
2022-05-01  661325  ->  -0.028
2022-06-01  667984  ->  1.007
2022-07-01  659750  ->  -1.233
2022-08-01  662999  ->  0.492
2022-09-01  661072  ->  -0.291
2022-10-01  666924  ->  0.885
2022-11-01  656410  ->  -1.576
2022-12-01  648305  ->  -1.235
2023-01-01  674646  ->  4.063
2023-02-01  664692  ->  -1.475
2023-03-01  655146  ->  -1.436
2023-04-01  658962  ->  0.582
2023-05-01  662303  ->  0.507
2023-06-01  664476  ->  0.328
2023-07-01  663391  ->  -0.163
2023-08-01  667632  ->  0.639
2023-09-01  671096  ->  0.519
2023-10-01  667815  ->  -0.489
2023-11-01  666419  ->  -0.209

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
