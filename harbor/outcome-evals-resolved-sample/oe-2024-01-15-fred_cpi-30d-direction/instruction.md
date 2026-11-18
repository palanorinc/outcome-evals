# Outcome Evals: oe-2024-01-15-fred_cpi-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-fred_cpi-30d-direction
Today is 2024-01-15.

Will the 12-month change in the U.S. Consumer Price Index (CPI-U, all items, seasonally adjusted; computed from the index) for February 2024 (the latest monthly reading dated on or before 2024-02-14) be above 3.32%, its value for December 2023?

Resolves on the latest reading dated on or before 2024-02-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_cpi`. If no such reading is published within 90 days after the deadline, the question is void.
Series: Consumer Price Index (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-01-01  282.543  ->  7.559
2022-02-01  284.5  ->  7.937
2022-03-01  287.674  ->  8.572
2022-04-01  288.561  ->  8.232
2022-05-01  291.298  ->  8.538
2022-06-01  294.957  ->  8.979
2022-07-01  294.913  ->  8.463
2022-08-01  295.097  ->  8.223
2022-09-01  296.349  ->  8.192
2022-10-01  298.007  ->  7.759
2022-11-01  298.786  ->  7.123
2022-12-01  298.832  ->  6.405
2023-01-01  300.42  ->  6.327
2023-02-01  301.45  ->  5.958
2023-03-01  301.821  ->  4.918
2023-04-01  302.845  ->  4.950
2023-05-01  303.334  ->  4.132
2023-06-01  304.014  ->  3.071
2023-07-01  304.609  ->  3.288
2023-08-01  306.082  ->  3.723
2023-09-01  307.276  ->  3.687
2023-10-01  307.696  ->  3.251
2023-11-01  308.148  ->  3.133
2023-12-01  308.741  ->  3.316

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
