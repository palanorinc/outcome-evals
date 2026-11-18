# Outcome Evals: oe-2024-04-15-rates.ust.par.3m-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-rates.ust.par.3m-90d-range
Today is 2024-04-15.

Will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) for 2024-07-14 (or the last business day before it with a published reading) be at least 5.45% and below 5.70%?

Resolves on the latest reading dated on or before 2024-07-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading
2024-03-11  5.48
2024-03-12  5.48
2024-03-13  5.48
2024-03-14  5.48
2024-03-15  5.48
2024-03-18  5.48
2024-03-19  5.48
2024-03-20  5.47
2024-03-21  5.48
2024-03-22  5.46
2024-03-25  5.46
2024-03-26  5.46
2024-03-27  5.45
2024-03-28  5.46
2024-04-01  5.44
2024-04-02  5.42
2024-04-03  5.42
2024-04-04  5.41
2024-04-05  5.43
2024-04-08  5.43
2024-04-09  5.43
2024-04-10  5.45
2024-04-11  5.45
2024-04-12  5.45

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
