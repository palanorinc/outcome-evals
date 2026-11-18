# Outcome Evals: oe-2026-04-15-rates.ust.par.3m-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-rates.ust.par.3m-30d-direction
Today is 2026-04-15.

Will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) for 2026-05-15 (or the last business day before it with a published reading) be above 3.71%, its value for 2026-04-14?

Resolves on the latest reading dated on or before 2026-05-15 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading
2026-03-12  3.72
2026-03-13  3.72
2026-03-16  3.72
2026-03-17  3.72
2026-03-18  3.73
2026-03-19  3.73
2026-03-20  3.74
2026-03-23  3.74
2026-03-24  3.74
2026-03-25  3.73
2026-03-26  3.73
2026-03-27  3.73
2026-03-30  3.71
2026-03-31  3.7
2026-04-01  3.7
2026-04-02  3.7
2026-04-03  3.71
2026-04-06  3.72
2026-04-07  3.71
2026-04-08  3.69
2026-04-09  3.68
2026-04-10  3.69
2026-04-13  3.71
2026-04-14  3.71

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
