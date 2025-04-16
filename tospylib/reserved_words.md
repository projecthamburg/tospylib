# Thinkscript Reserved Words and Terms
This file contains definitions of all Thinkscript reserved words and their Python equivalents for tospylib indicators.

## Average
Thinkscript documentation: Returns the average value for data over N bars (simple moving average). In tospylib, this is implemented as `simple_moving_avg()` function.

## ExpAverage
Thinkscript documentation: Returns the exponential moving average of data over N bars. In tospylib, this is implemented as `mov_avg_exponential()` function.

## WildersAverage
Thinkscript documentation: Returns the Wilder's smoothing average of data over N bars. In tospylib, this is implemented through `IndicatorUtils.wilders_moving_avg()` method.

## StDev
Thinkscript documentation: Returns the standard deviation of data over N bars. In tospylib, this is implemented through `IndicatorUtils.stdev()` method.

## Highest / Lowest
Thinkscript documentation: Returns the highest/lowest value of data over N bars. In tospylib, highest is implemented through `IndicatorUtils.highest()` method.

## Crosses Above / Crosses Below
Thinkscript documentation: Returns true when one plot crosses above/below another. In tospylib, these are implemented as utility methods for generating trading signals.

## AggregationPeriod
Thinkscript documentation: Defines the timeframe over which the indicator is calculated. In tospylib, this is implemented as an Enum in `tospylib.enums.AggregationPeriod` with values like MINUTE, FIVE_MIN, HOUR, DAY, etc.
