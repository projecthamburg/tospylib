"""
Simple Moving Average (SMA)
Thinkscript reference: Average
Inputs:
    price: Series (input price, usually close)
    length: int (bars for average, default 9)
    displace: int (how many bars to offset SMA, default 0)
    display_index: pandas.Index or None (optional; index to broadcast SMA for display)
Output:
    pd.Series with SMA values
Dependencies:
    IndicatorUtils.simple_moving_avg
"""

import pandas as pd
from ..indicator_utils import IndicatorUtils

def simple_moving_avg(
    price,
    length=9,
    displace=0,
    display_index=None
):
    """
    Simple Moving Average (SMA)
    Thinkscript: Average
    Params:
        price: pd.Series
        length: int, number of bars to average
        displace: int, shift for indicator (Thinkscript style)
        display_index: pandas.Index or None for multi-timeframe alignment
    Returns:
        pd.Series
    """
    price = pd.Series(price)
    if displace != 0:
        price = price.shift(-displace)
    sma = IndicatorUtils.simple_moving_avg(price, length)
    
    if display_index is not None:
        sma = sma.reindex(display_index, method='ffill')
    
    return sma
