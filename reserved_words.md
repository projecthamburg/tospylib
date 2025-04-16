# Reserved Words Reference

This document provides a reference for the reserved words used in TospyLib and their translations to different technical analysis platforms.

## Average
Thinkscript documentation: Returns the average value for data over N bars (simple moving average).
TospyLib equivalent: `simple_moving_avg`

## ExpAverage
Thinkscript documentation: Returns the exponential moving average of data over N bars.
TospyLib equivalent: `mov_avg_exponential`

## WildersAverage
Thinkscript documentation: Returns the Wilder's smoothing average of data over N bars.
TospyLib equivalent: `wilders_moving_avg`

## StDev
Thinkscript documentation: Returns the standard deviation of data over N bars.
TospyLib equivalent: `standard_deviation`

## Highest / Lowest
Thinkscript documentation: Returns the highest/lowest value of data over N bars.
TospyLib equivalent: `highest` / `lowest`

## Crosses Above / Crosses Below
Thinkscript documentation: Returns true when data1 crosses above/below data2.
TospyLib equivalent: `crosses_above` / `crosses_below`

## AggregationPeriod
Thinkscript documentation: Specifies the aggregation period for data (DAY, WEEK, MONTH).
TospyLib equivalent: `timeframe` parameter in functions like `pivot_points`