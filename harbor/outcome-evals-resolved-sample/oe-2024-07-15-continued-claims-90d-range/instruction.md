# Outcome Evals: oe-2024-07-15-continued-claims-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-continued-claims-90d-range
Today is 2024-07-15.

Will U.S. continued unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2024-10-13 (expected: 2024-10-12) be at least 1,680,000 and below 1,890,000?

Resolves on the latest reading dated on or before 2024-10-13 (and no more than 8 days before it), using the reading itself, as published in series `continued-claims`. If no such reading is published within 58 days after the deadline, the question is void.
Series: Continued jobless claims (U.S. Department of Labor), unit: count.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading
2024-01-20  1.829e+06
2024-01-27  1.804e+06
2024-02-03  1.8e+06
2024-02-10  1.784e+06
2024-02-17  1.802e+06
2024-02-24  1.788e+06
2024-03-02  1.8e+06
2024-03-09  1.79e+06
2024-03-16  1.807e+06
2024-03-23  1.788e+06
2024-03-30  1.81e+06
2024-04-06  1.797e+06
2024-04-13  1.781e+06
2024-04-20  1.769e+06
2024-04-27  1.788e+06
2024-05-04  1.792e+06
2024-05-11  1.791e+06
2024-05-18  1.808e+06
2024-05-25  1.804e+06
2024-06-01  1.821e+06
2024-06-08  1.83e+06
2024-06-15  1.839e+06
2024-06-22  1.862e+06
2024-06-29  1.853e+06

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
