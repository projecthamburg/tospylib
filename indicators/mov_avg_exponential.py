"""
Exponential Moving Average (EMA)
Thinkscript reference: ExpAverage
Inputs:
    price: Series (input price, usually close)
    length: int (bars for average, default 9)
    displace: int (how many bars to offset EMA, default 0)
    show_breakout_signals: bool (default False)
    display_index: pandas.Index or None (optional; index to broadcast EMA for display)
Output:
    DataFrame with columns: 'AvgExp', 'UpSignal', 'DownSignal'
Dependencies:
    IndicatorUtils.exp_moving_avg
"""
import pandas as pd
import numpy as np
from ..indicator_utils import IndicatorUtils

def mov_avg_exponential(
    price,
    length=9,
    displace=0,
    show_breakout_signals=False,
    display_index=None
):
    """
    Exponential Moving Average (EMA)
    Thinkscript: ExpAverage
    Params:
        price: pd.Series
        length: int
        displace: int
        show_breakout_signals: bool
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "AvgExp", "UpSignal", "DownSignal"
    """
    price = pd.Series(price)
    if displace != 0:
        price = price.shift(-displace)
    ema = IndicatorUtils.exp_moving_avg(price, length)
    
    # Generate breakout signals if requested
    up_signal = IndicatorUtils.crosses_above(price, ema) if show_breakout_signals else pd.Series(np.nan, index=price.index)
    down_signal = IndicatorUtils.crosses_below(price, ema) if show_breakout_signals else pd.Series(np.nan, index=price.index)
    
    # Create result DataFrame
    result = pd.DataFrame({"AvgExp": ema, "UpSignal": up_signal, "DownSignal": down_signal}, index=price.index)
    
    if display_index is not None:
        result = result.reindex(display_index, method='ffill')
    
    return result
