# Outcome Evals: oe-2025-07-15-continued-claims-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-continued-claims-90d-direction
Today is 2025-07-15.

Will U.S. continued unemployment insurance claims (DOL, seasonally adjusted, week ending) for the latest weekly reading dated on or before 2025-10-13 (expected: 2025-10-11) be above 1,952,000, its value for the week dated 2025-06-28?

Resolves on the latest reading dated on or before 2025-10-13 (and no more than 8 days before it), using the reading itself, as published in series `continued-claims`. If no such reading is published within 58 days after the deadline, the question is void.
Series: Continued jobless claims (U.S. Department of Labor), unit: count.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading
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
2025-04-05  1.876e+06
2025-04-12  1.84e+06
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
