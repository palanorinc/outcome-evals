# Outcome Evals: oe-2024-04-15-fred_nfp-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-fred_nfp-90d-range
Today is 2024-04-15.

Will the one-month change in U.S. nonfarm payrolls (BLS, seasonally adjusted, thousands of jobs) for July 2024 (the latest monthly reading dated on or before 2024-07-14) be at least 100 thousand and below 325 thousand?

Resolves on the latest reading dated on or before 2024-07-14 (and no more than 31 days before it), using the reading minus the reading 1 month earlier, as published in series `fred_nfp`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Nonfarm Payrolls (U.S. Bureau of Labor Statistics), unit: thousands of persons.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-04-01  151623  ->  308.000
2022-05-01  151924  ->  301.000
2022-06-01  152358  ->  434.000
2022-07-01  153072  ->  714.000
2022-08-01  153362  ->  290.000
2022-09-01  153582  ->  220.000
2022-10-01  153939  ->  357.000
2022-11-01  154242  ->  303.000
2022-12-01  154342  ->  100.000
2023-01-01  154776  ->  434.000
2023-02-01  155066  ->  290.000
2023-03-01  155134  ->  68.000
2023-04-01  155375  ->  241.000
2023-05-01  155655  ->  280.000
2023-06-01  155880  ->  225.000
2023-07-01  156043  ->  163.000
2023-08-01  156261  ->  218.000
2023-09-01  156417  ->  156.000
2023-10-01  156576  ->  159.000
2023-11-01  156703  ->  127.000
2023-12-01  156857  ->  154.000
2024-01-01  157032  ->  175.000
2024-02-01  157238  ->  206.000
2024-03-01  157466  ->  228.000

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
