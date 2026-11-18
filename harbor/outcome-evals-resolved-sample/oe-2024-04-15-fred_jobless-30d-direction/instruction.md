# Outcome Evals: oe-2024-04-15-fred_jobless-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-fred_jobless-30d-direction
Today is 2024-04-15.

Will U.S. initial unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2024-05-15 (expected: 2024-05-11) be above 213,000, its value for the week dated 2024-04-06?

Resolves on the latest reading dated on or before 2024-05-15 (and no more than 8 days before it), using the reading itself, as published in series `fred_jobless`. If no such reading is published within 51 days after the deadline, the question is void.
Series: Initial Jobless Claims (U.S. Department of Labor), unit: count.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading
2023-10-28  217000
2023-11-04  216000
2023-11-11  230000
2023-11-18  213000
2023-11-25  213000
2023-12-02  215000
2023-12-09  203000
2023-12-16  209000
2023-12-23  212000
2023-12-30  200000
2024-01-06  201000
2024-01-13  195000
2024-01-20  224000
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
