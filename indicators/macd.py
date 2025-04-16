"""
MACD Indicator
Thinkscript reference: MACD
Inputs:
    price: Series
    fast_length: int (default 12)
    slow_length: int (default 26)
    macd_length: int (default 9)
    display_index: pandas.Index or None
Outputs:
    DataFrame: 'Value', 'Avg', 'Diff'
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def macd(
    price,
    fast_length=12,
    slow_length=26,
    macd_length=9,
    display_index=None
):
    """
    MACD Indicator
    Thinkscript: MACD
    Params:
        price: pd.Series
        fast_length: int
        slow_length: int
        macd_length: int
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "Value", "Avg", "Diff"
    """
    fast_ema = IndicatorUtils.exp_moving_avg(price, fast_length)
    slow_ema = IndicatorUtils.exp_moving_avg(price, slow_length)
    value = fast_ema - slow_ema
    avg = IndicatorUtils.exp_moving_avg(value, macd_length)
    diff = value - avg
    result = pd.DataFrame({
        "Value": value,
        "Avg": avg,
        "Diff": diff,
    }, index=price.index)
    if display_index is not None:
        result = result.reindex(display_index, method="ffill")
    return result
