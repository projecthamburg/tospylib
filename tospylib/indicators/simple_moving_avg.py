"""
SimpleMovingAvg Indicator
Thinkscript formula reference: SimpleMovingAvg
Inputs: input price=close; input length=9; input displace=0; input showBreakoutSignals=no;
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd

def simple_moving_avg(price, length=9, displace=0, display_index=None):
    """
    Simple Moving Average (SMA), Thinkscript-style.
    price: pandas Series of prices
    length: int, periods for moving average
    displace: int, offset, Thinkscript style (negative=look back, positive=look forward)
    display_index: optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    """
    price_shifted = pd.Series(price).shift(-displace)
    sma = price_shifted.rolling(length, min_periods=1).mean()
    if display_index is not None:
        sma = sma.reindex(display_index, method="ffill")
    return sma
