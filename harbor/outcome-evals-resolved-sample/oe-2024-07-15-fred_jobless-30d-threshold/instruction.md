# Outcome Evals: oe-2024-07-15-fred_jobless-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-fred_jobless-30d-threshold
Today is 2024-07-15.

Will U.S. initial unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2024-08-14 (expected: 2024-08-10) be below 205,000?

Resolves on the latest reading dated on or before 2024-08-14 (and no more than 8 days before it), using the reading itself, as published in series `fred_jobless`. If no such reading is published within 51 days after the deadline, the question is void.
Series: Initial Jobless Claims (U.S. Department of Labor), unit: count.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading
2024-01-27  226000
2024-02-03  213000
2024-02-10  213000
2024-02-17  202000
2024-02-24  212000
2024-03-02  213000
2024-03-09  213000
2024-03-16  213000
2024-03-23  214000
2024-03-30  223000
2024-04-06  213000
2024-04-13  212000
2024-04-20  209000
2024-04-27  207000
2024-05-04  230000
2024-05-11  222000
2024-05-18  216000
2024-05-25  220000
2024-06-01  227000
2024-06-08  240000
2024-06-15  236000
2024-06-22  233000
2024-06-29  238000
2024-07-06  223000

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
