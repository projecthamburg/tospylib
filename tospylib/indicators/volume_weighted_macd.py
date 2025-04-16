"""
Volume Weighted MACD
Thinkscript reference: VolumeWeightedMACD
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
Inputs:
    close: Series
    volume: Series
    fast_length: int (default 12)
    slow_length: int (default 26)
    macd_length: int (default 9)
    display_index: pandas.Index or None
Outputs:
    DataFrame: Value, Avg, Diff
"""
import pandas as pd
import numpy as np
from ..indicator_utils import IndicatorUtils

def volume_weighted_macd(close, volume, fast_length=12, slow_length=26, macd_length=9, display_index=None):
    vw_fast = (volume * close).rolling(window=fast_length, min_periods=1).sum() / volume.rolling(window=fast_length, min_periods=1).sum()
    vw_slow = (volume * close).rolling(window=slow_length, min_periods=1).sum() / volume.rolling(window=slow_length, min_periods=1).sum()
    value = vw_fast - vw_slow
    avg = IndicatorUtils.exp_moving_avg(value, macd_length)
    diff = value - avg
    result = pd.DataFrame({
        "Value": value,
        "Avg": avg,
        "Diff": diff,
    }, index=close.index)
    if display_index is not None:
        result = result.reindex(display_index, method='ffill')
    return result
