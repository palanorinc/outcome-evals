# Outcome Evals: oe-2025-04-15-rates.ust.par.10y-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-rates.ust.par.10y-90d-direction
Today is 2025-04-15.

Will the 10-year U.S. Treasury par yield (Treasury daily par yield curve) for 2025-07-14 (or the last business day before it with a published reading) be above 4.38%, its value for 2025-04-14?

Resolves on the latest reading dated on or before 2025-07-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 10-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2025-03-12  4.32
2025-03-13  4.27
2025-03-14  4.31
2025-03-17  4.31
2025-03-18  4.29
2025-03-19  4.25
2025-03-20  4.24
2025-03-21  4.25
2025-03-24  4.34
2025-03-25  4.31
2025-03-26  4.35
2025-03-27  4.38
2025-03-28  4.27
2025-03-31  4.23
2025-04-01  4.17
2025-04-02  4.2
2025-04-03  4.06
2025-04-04  4.01
2025-04-07  4.15
2025-04-08  4.26
2025-04-09  4.34
2025-04-10  4.4
2025-04-11  4.48
2025-04-14  4.38

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
