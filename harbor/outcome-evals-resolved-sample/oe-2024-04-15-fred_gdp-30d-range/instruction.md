# Outcome Evals: oe-2024-04-15-fred_gdp-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-fred_gdp-30d-range
Today is 2024-04-15.

Will U.S. real GDP growth, quarter on quarter at an annual rate (BEA, chained dollars, seasonally adjusted; computed from the level) for Q2 2024 (the latest quarterly reading dated on or before 2024-05-15) be at least 2.00% and below 5.00%?

Resolves on the latest reading dated on or before 2024-05-15 (and no more than 92 days before it), using the percent change from the reading 1 quarter earlier, at an annual rate, as published in series `fred_gdp`. If no such reading is published within 170 days after the deadline, the question is void.
Series: Real GDP (U.S. Bureau of Economic Analysis), unit: index.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2018-01-01  20044.1  ->  3.294
2018-04-01  20150.5  ->  2.140
2018-07-01  20276.2  ->  2.518
2018-10-01  20304.9  ->  0.568
2019-01-01  20431.6  ->  2.521
2019-04-01  20602.3  ->  3.383
2019-07-01  20843.3  ->  4.763
2019-10-01  20985.4  ->  2.756
2020-01-01  20709.2  ->  -5.162
2020-04-01  19078  ->  -27.976
2020-07-01  20558.9  ->  34.855
2020-10-01  20791.9  ->  4.612
2021-01-01  21106.6  ->  6.193
2021-04-01  21474.1  ->  7.148
2021-07-01  21641.7  ->  3.159
2021-10-01  22001.6  ->  6.821
2022-01-01  21945.7  ->  -1.013
2022-04-01  21976.3  ->  0.559
2022-07-01  22124.4  ->  2.723
2022-10-01  22272.5  ->  2.706
2023-01-01  22456.9  ->  3.353
2023-04-01  22577.6  ->  2.166
2023-07-01  22828.8  ->  4.526
2023-10-01  23033.2  ->  3.631

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
