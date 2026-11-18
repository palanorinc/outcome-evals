# Outcome Evals: oe-2024-10-15-fred_unemployment-30d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-10-15-fred_unemployment-30d-number
Today is 2024-10-15.

What will the U.S. unemployment rate (BLS, seasonally adjusted) be for November 2024 (the latest monthly reading dated on or before 2024-11-14)?

Resolves on the latest reading dated on or before 2024-11-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_unemployment`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Unemployment Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2024-10-15 (latest 24, oldest first):
date  reading
2022-10-01  3.6
2022-11-01  3.6
2022-12-01  3.5
2023-01-01  3.5
2023-02-01  3.6
2023-03-01  3.5
2023-04-01  3.4
2023-05-01  3.6
2023-06-01  3.6
2023-07-01  3.5
2023-08-01  3.7
2023-09-01  3.7
2023-10-01  3.9
2023-11-01  3.7
2023-12-01  3.8
2024-01-01  3.7
2024-02-01  3.9
2024-03-01  3.9
2024-04-01  3.9
2024-05-01  3.9
2024-06-01  4.1
2024-07-01  4.2
2024-08-01  4.2
2024-09-01  4.1

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
