# Outcome Evals: oe-2024-01-15-fred_lfpr-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-fred_lfpr-90d-range
Today is 2024-01-15.

Will the U.S. labor force participation rate (BLS, seasonally adjusted) for April 2024 (the latest monthly reading dated on or before 2024-04-14) be at least 62.4% and below 62.7%?

Resolves on the latest reading dated on or before 2024-04-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_lfpr`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Labor Force Participation Rate (U.S. Bureau of Labor Statistics), unit: %.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading
2022-01-01  62.2
2022-02-01  62.3
2022-03-01  62.4
2022-04-01  62.2
2022-05-01  62.3
2022-06-01  62.2
2022-07-01  62.1
2022-08-01  62.3
2022-09-01  62.2
2022-10-01  62.2
2022-11-01  62.1
2022-12-01  62.3
2023-01-01  62.4
2023-02-01  62.5
2023-03-01  62.6
2023-04-01  62.6
2023-05-01  62.6
2023-06-01  62.6
2023-07-01  62.6
2023-08-01  62.8
2023-09-01  62.7
2023-10-01  62.6
2023-11-01  62.8
2023-12-01  62.5

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
