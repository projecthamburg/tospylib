"""
ADX (Average Directional Index)
Thinkscript reference: ADX (as in DMI or Wilders' average)
Inputs:
    high: Series
    low: Series
    close: Series
    length: int (default 14)
    display_index: pandas.Index or None
Outputs:
    Series: ADX values (trend strength)
"""
import pandas as pd
import numpy as np
from ..indicator_utils import IndicatorUtils

def adx(
    high,
    low,
    close,
    length=14,
    display_index=None
):
    """
    Average Directional Index (ADX)
    Thinkscript: ADX
    Params:
        high: pd.Series
        low: pd.Series
        close: pd.Series
        length: int
        display_index: pandas.Index or None
    Returns:
        pd.Series (adx)
    """
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    atr = IndicatorUtils.wilders_moving_avg(tr, length)
    plus_di = 100 * IndicatorUtils.wilders_moving_avg(plus_dm, length) / atr
    minus_di = 100 * IndicatorUtils.wilders_moving_avg(minus_dm, length) / atr
    dx = 100 * (abs(plus_di - minus_di)) / (plus_di + minus_di)
    adx = IndicatorUtils.wilders_moving_avg(dx, length)
    adx = pd.Series(adx, index=high.index)
    if display_index is not None:
        adx = adx.reindex(display_index, method='ffill')
    return adx