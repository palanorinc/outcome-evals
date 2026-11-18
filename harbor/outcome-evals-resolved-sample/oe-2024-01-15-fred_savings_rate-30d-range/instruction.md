# Outcome Evals: oe-2024-01-15-fred_savings_rate-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-fred_savings_rate-30d-range
Today is 2024-01-15.

Will the U.S. personal saving rate (BEA, seasonally adjusted) for February 2024 (the latest monthly reading dated on or before 2024-02-14) be at least 5.8% and below 6.8%?

Resolves on the latest reading dated on or before 2024-02-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_savings_rate`. If no such reading is published within 107 days after the deadline, the question is void.
Series: Personal Savings Rate (U.S. Bureau of Economic Analysis), unit: %.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading
2021-12-01  6.8
2022-01-01  4.3
2022-02-01  4.2
2022-03-01  3.3
2022-04-01  2.7
2022-05-01  2.6
2022-06-01  2.4
2022-07-01  3.4
2022-08-01  3.4
2022-09-01  3.6
2022-10-01  3.6
2022-11-01  4
2022-12-01  4.4
2023-01-01  5
2023-02-01  5.6
2023-03-01  6.1
2023-04-01  6.1
2023-05-01  6.4
2023-06-01  6.3
2023-07-01  6.2
2023-08-01  6.3
2023-09-01  6
2023-10-01  6.2
2023-11-01  6.4

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
