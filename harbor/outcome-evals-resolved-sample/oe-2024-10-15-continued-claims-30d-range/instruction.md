# Outcome Evals: oe-2024-10-15-continued-claims-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-10-15-continued-claims-30d-range
Today is 2024-10-15.

Will U.S. continued unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2024-11-14 (expected: 2024-11-09) be at least 1,780,000 and below 1,880,000?

Resolves on the latest reading dated on or before 2024-11-14 (and no more than 8 days before it), using the reading itself, as published in series `continued-claims`. If no such reading is published within 58 days after the deadline, the question is void.
Series: Continued jobless claims (U.S. Department of Labor), unit: count.

Readings published by 2024-10-15 (latest 24, oldest first):
date  reading
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
2024-07-06  1.864e+06
2024-07-13  1.848e+06
2024-07-20  1.873e+06
2024-07-27  1.871e+06
2024-08-03  1.863e+06
2024-08-10  1.855e+06
2024-08-17  1.862e+06
2024-08-24  1.847e+06
2024-08-31  1.845e+06
2024-09-07  1.825e+06
2024-09-14  1.831e+06
2024-09-21  1.825e+06
2024-09-28  1.858e+06

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
