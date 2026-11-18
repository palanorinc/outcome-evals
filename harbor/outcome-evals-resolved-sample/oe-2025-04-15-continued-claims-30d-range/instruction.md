# Outcome Evals: oe-2025-04-15-continued-claims-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-continued-claims-30d-range
Today is 2025-04-15.

Will U.S. continued unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2025-05-15 (expected: 2025-05-10) be at least 1,780,000 and below 1,880,000?

Resolves on the latest reading dated on or before 2025-05-15 (and no more than 8 days before it), using the reading itself, as published in series `continued-claims`. If no such reading is published within 58 days after the deadline, the question is void.
Series: Continued jobless claims (U.S. Department of Labor), unit: count.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2024-10-19  1.853e+06
2024-10-26  1.876e+06
2024-11-02  1.87e+06
2024-11-09  1.887e+06
2024-11-16  1.887e+06
2024-11-23  1.866e+06
2024-11-30  1.859e+06
2024-12-07  1.865e+06
2024-12-14  1.881e+06
2024-12-21  1.833e+06
2024-12-28  1.868e+06
2025-01-04  1.85e+06
2025-01-11  1.891e+06
2025-01-18  1.854e+06
2025-01-25  1.876e+06
2025-02-01  1.84e+06
2025-02-08  1.862e+06
2025-02-15  1.849e+06
2025-02-22  1.889e+06
2025-03-01  1.857e+06
2025-03-08  1.876e+06
2025-03-15  1.852e+06
2025-03-22  1.889e+06
2025-03-29  1.852e+06

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
