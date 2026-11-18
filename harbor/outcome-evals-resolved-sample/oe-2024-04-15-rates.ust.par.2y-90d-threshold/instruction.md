# Outcome Evals: oe-2024-04-15-rates.ust.par.2y-90d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-rates.ust.par.2y-90d-threshold
Today is 2024-04-15.

Will the 2-year U.S. Treasury par yield (Treasury daily par yield curve) for 2024-07-14 (or the last business day before it with a published reading) be above 5.15%?

Resolves on the latest reading dated on or before 2024-07-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.2y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 2-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading
2024-03-11  4.51
2024-03-12  4.58
2024-03-13  4.61
2024-03-14  4.68
2024-03-15  4.72
2024-03-18  4.73
2024-03-19  4.68
2024-03-20  4.59
2024-03-21  4.62
2024-03-22  4.59
2024-03-25  4.54
2024-03-26  4.56
2024-03-27  4.54
2024-03-28  4.59
2024-04-01  4.72
2024-04-02  4.7
2024-04-03  4.68
2024-04-04  4.65
2024-04-05  4.73
2024-04-08  4.78
2024-04-09  4.74
2024-04-10  4.97
2024-04-11  4.93
2024-04-12  4.88

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
