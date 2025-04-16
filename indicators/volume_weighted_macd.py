"""
Volume Weighted MACD
Thinkscript reference: VolumeWeightedMACD
Inputs:
    close: Series
    volume: Series
    fast_length: int (default 12)
    slow_length: int (default 26)
    macd_length: int (default 9)
    display_index: pandas.Index or None
Outputs:
    DataFrame: Value, Avg, Diff, ZeroLine
"""
import pandas as pd
import numpy as np
from ..indicator_utils import IndicatorUtils

def volume_weighted_macd(
    close,
    volume,
    fast_length=12,
    slow_length=26,
    macd_length=9,
    display_index=None
):
    """
    Volume Weighted MACD
    Thinkscript: VolumeWeightedMACD
    Params:
        close: pd.Series
        volume: pd.Series
        fast_length: int
        slow_length: int
        macd_length: int
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "Value", "Avg", "Diff", "ZeroLine"
    """
    vw_fast = (volume * close).rolling(window=fast_length, min_periods=1).sum() / volume.rolling(window=fast_length, min_periods=1).sum()
    vw_slow = (volume * close).rolling(window=slow_length, min_periods=1).sum() / volume.rolling(window=slow_length, min_periods=1).sum()
    value = vw_fast - vw_slow
    avg = IndicatorUtils.exp_moving_avg(value, macd_length)
    diff = value - avg
    zero_line = pd.Series(0, index=close.index)
    result = pd.DataFrame({
        "Value": value,
        "Avg": avg,
        "Diff": diff,
        "ZeroLine": zero_line,
    }, index=close.index)
    if display_index is not None:
        result = result.reindex(display_index, method='ffill')
    return result
