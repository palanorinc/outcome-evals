# Outcome Evals: oe-2025-10-15-continued-claims-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-10-15-continued-claims-90d-direction
Today is 2025-10-15.

Will U.S. continued unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2026-01-13 (expected: 2026-01-10) be above 1,929,000, its value for the week dated 2025-09-27?

Resolves on the latest reading dated on or before 2026-01-13 (and no more than 8 days before it), using the reading itself, as published in series `continued-claims`. If no such reading is published within 58 days after the deadline, the question is void.
Series: Continued jobless claims (U.S. Department of Labor), unit: count.

Readings published by 2025-10-15 (latest 24, oldest first):
date  reading
2025-04-19  1.906e+06
2025-04-26  1.876e+06
2025-05-03  1.884e+06
2025-05-10  1.889e+06
2025-05-17  1.917e+06
2025-05-24  1.896e+06
2025-05-31  1.947e+06
2025-06-07  1.935e+06
2025-06-14  1.96e+06
2025-06-21  1.954e+06
2025-06-28  1.952e+06
2025-07-05  1.949e+06
2025-07-12  1.941e+06
2025-07-19  1.936e+06
2025-07-26  1.963e+06
2025-08-02  1.942e+06
2025-08-09  1.957e+06
2025-08-16  1.942e+06
2025-08-23  1.937e+06
2025-08-30  1.927e+06
2025-09-06  1.925e+06
2025-09-13  1.916e+06
2025-09-20  1.921e+06
2025-09-27  1.929e+06

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
