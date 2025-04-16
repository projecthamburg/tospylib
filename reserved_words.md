# Reserved Words Reference

This document provides a reference for the reserved words used in TospyLib and their translations to different technical analysis platforms.

## Variable Declarations
### def
Thinkscript documentation: Defines a variable that can be used in formulas. Variables are calculated once and can be reused in other calculations.
TospyLib equivalent: Regular Python variable assignment

### rec
Thinkscript documentation: Defines a recursive variable that can reference its previous values. Values are calculated chronologically and can use values from previous bars.
TospyLib equivalent: Custom implementation in indicator functions

### input
Thinkscript documentation: Defines a parameter that can be modified by the user. Used for customizable study parameters.
TospyLib equivalent: Function parameters with default values

### declare
Thinkscript documentation: Used to specify study attributes like lower/upper for indicator placement.
TospyLib equivalent: Function decorators or parameters

## Plotting
### plot
Thinkscript documentation: Creates a visual representation of data on the chart.
TospyLib equivalent: Return values from indicator functions

### SetPaintingStrategy
Thinkscript documentation: Defines how the plot should be displayed (line, histogram, arrows, etc.).
TospyLib equivalent: Plotting parameters in visualization functions

## Mathematical Functions
### Average
Thinkscript documentation: Returns the average value for data over N bars (simple moving average).
TospyLib equivalent: `simple_moving_avg`

### ExpAverage
Thinkscript documentation: Returns the exponential moving average of data over N bars.
TospyLib equivalent: `mov_avg_exponential`

### WildersAverage
Thinkscript documentation: Returns the Wilder's smoothing average of data over N bars.
TospyLib equivalent: `wilders_moving_avg`

### StDev
Thinkscript documentation: Returns the standard deviation of data over N bars.
TospyLib equivalent: `standard_deviation`

### Highest / Lowest
Thinkscript documentation: Returns the highest/lowest value of data over N bars.
TospyLib equivalent: `highest` / `lowest`

### Crosses Above / Crosses Below
Thinkscript documentation: Returns true when data1 crosses above/below data2.
TospyLib equivalent: `crosses_above` / `crosses_below`

## Time and Aggregation
### AggregationPeriod
Thinkscript documentation: Specifies the aggregation period for data (DAY, WEEK, MONTH).
TospyLib equivalent: `timeframe` parameter in functions like `pivot_points`

### GetTime
Thinkscript documentation: Returns the time of the current bar.
TospyLib equivalent: Timestamp handling in data processing

### GetYYYYMMDD
Thinkscript documentation: Returns the date of the current bar in YYYYMMDD format.
TospyLib equivalent: Date formatting in data processing

## Price Data
### close
Thinkscript documentation: The closing price of the current bar.
TospyLib equivalent: `close` parameter in indicator functions

### high
Thinkscript documentation: The highest price of the current bar.
TospyLib equivalent: `high` parameter in indicator functions

### low
Thinkscript documentation: The lowest price of the current bar.
TospyLib equivalent: `low` parameter in indicator functions

### open
Thinkscript documentation: The opening price of the current bar.
TospyLib equivalent: `open` parameter in indicator functions

### volume
Thinkscript documentation: The trading volume of the current bar.
TospyLib equivalent: `volume` parameter in indicator functions