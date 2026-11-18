# Outcome Evals: oe-2026-07-15-fred_jobless-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-07-15-fred_jobless-30d-range
Today is 2026-07-15.

Will U.S. initial unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2026-08-14 (expected: 2026-08-08) be at least 200,000 and below 225,000?

Resolves on the latest reading dated on or before 2026-08-14 (and no more than 8 days before it), using the reading itself, as published in series `fred_jobless`. If no such reading is published within 51 days after the deadline, the question is void.
Series: Initial Jobless Claims (U.S. Department of Labor), unit: count.

Readings published by 2026-07-15 (latest 24, oldest first):
date  reading
2026-01-24  211000
2026-01-31  230000
2026-02-07  230000
2026-02-14  208000
2026-02-21  211000
2026-02-28  214000
2026-03-07  213000
2026-03-14  205000
2026-03-21  211000
2026-03-28  203000
2026-04-04  218000
2026-04-11  208000
2026-04-18  215000
2026-04-25  190000
2026-05-02  199000
2026-05-09  212000
2026-05-16  210000
2026-05-23  212000
2026-05-30  225000
2026-06-06  230000
2026-06-13  227000
2026-06-20  216000
2026-06-27  217000
2026-07-04  217000

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
