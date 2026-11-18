# Outcome Evals: oe-2024-04-15-auto-sales-30d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-auto-sales-30d-number
Today is 2024-04-15.

What will U.S. total light-vehicle sales (BEA, seasonally adjusted annual rate, millions of units) be for May 2024 (the latest monthly reading dated on or before 2024-05-15)?

Resolves on the latest reading dated on or before 2024-05-15 (and no more than 31 days before it), using the reading itself, as published in series `auto-sales`. If no such reading is published within 83 days after the deadline, the question is void.
Series: Total light-vehicle sales (U.S. Bureau of Economic Analysis), unit: units.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading
2022-04-01  14.566
2022-05-01  13.308
2022-06-01  13.815
2022-07-01  13.789
2022-08-01  14.076
2022-09-01  14.078
2022-10-01  15.195
2022-11-01  14.643
2022-12-01  13.864
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

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
