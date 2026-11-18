# Outcome Evals: oe-2026-07-15-rates.ust.par.3m-90d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-07-15-rates.ust.par.3m-90d-number
Today is 2026-07-15.

What will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) be for 2026-10-13 (or the last business day before it with a published reading)?

Resolves on the latest reading dated on or before 2026-10-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2026-07-15 (latest 24, oldest first):
date  reading
2026-06-09  3.79
2026-06-10  3.79
2026-06-11  3.78
2026-06-12  3.78
2026-06-15  3.79
2026-06-16  3.79
2026-06-17  3.83
2026-06-18  3.83
2026-06-22  3.85
2026-06-23  3.85
2026-06-24  3.85
2026-06-25  3.84
2026-06-26  3.83
2026-06-29  3.87
2026-06-30  3.87
2026-07-01  3.85
2026-07-02  3.82
2026-07-06  3.87
2026-07-07  3.86
2026-07-08  3.87
2026-07-09  3.83
2026-07-10  3.85
2026-07-13  3.89
2026-07-14  3.84

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
