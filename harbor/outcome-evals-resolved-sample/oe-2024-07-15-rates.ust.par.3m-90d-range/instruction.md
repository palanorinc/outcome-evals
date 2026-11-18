# Outcome Evals: oe-2024-07-15-rates.ust.par.3m-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-rates.ust.par.3m-90d-range
Today is 2024-07-15.

Will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) for 2024-10-13 (or the last business day before it with a published reading) be at least 5.40% and below 5.70%?

Resolves on the latest reading dated on or before 2024-10-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading
2024-06-07  5.52
2024-06-10  5.52
2024-06-11  5.52
2024-06-12  5.51
2024-06-13  5.51
2024-06-14  5.51
2024-06-17  5.52
2024-06-18  5.5
2024-06-20  5.5
2024-06-21  5.49
2024-06-24  5.5
2024-06-25  5.49
2024-06-26  5.5
2024-06-27  5.49
2024-06-28  5.48
2024-07-01  5.47
2024-07-02  5.47
2024-07-03  5.47
2024-07-05  5.46
2024-07-08  5.46
2024-07-09  5.46
2024-07-10  5.46
2024-07-11  5.44
2024-07-12  5.43

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
