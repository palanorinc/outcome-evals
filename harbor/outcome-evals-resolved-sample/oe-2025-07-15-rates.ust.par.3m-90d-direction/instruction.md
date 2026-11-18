# Outcome Evals: oe-2025-07-15-rates.ust.par.3m-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-rates.ust.par.3m-90d-direction
Today is 2025-07-15.

Will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) for 2025-10-13 (or the last business day before it with a published reading) be above 4.42%, its value for 2025-07-14?

Resolves on the latest reading dated on or before 2025-10-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading
2025-06-09  4.44
2025-06-10  4.45
2025-06-11  4.45
2025-06-12  4.46
2025-06-13  4.45
2025-06-16  4.43
2025-06-17  4.42
2025-06-18  4.42
2025-06-20  4.39
2025-06-23  4.38
2025-06-24  4.38
2025-06-25  4.38
2025-06-26  4.39
2025-06-27  4.39
2025-06-30  4.41
2025-07-01  4.4
2025-07-02  4.41
2025-07-03  4.42
2025-07-07  4.42
2025-07-08  4.42
2025-07-09  4.42
2025-07-10  4.42
2025-07-11  4.41
2025-07-14  4.42

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
