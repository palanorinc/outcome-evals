# Outcome Evals: oe-2024-07-15-fred_unemployment-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-fred_unemployment-90d-direction
Today is 2024-07-15.

Will the U.S. unemployment rate (BLS, seasonally adjusted) for October 2024 (the latest monthly reading dated on or before 2024-10-13) be above 4.1%, its value for June 2024?

Resolves on the latest reading dated on or before 2024-10-13 (and no more than 31 days before it), using the reading itself, as published in series `fred_unemployment`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Unemployment Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading
2022-07-01  3.5
2022-08-01  3.6
2022-09-01  3.5
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
