"""
Stochastic Fast Indicator
Thinkscript reference: StochasticFast
Inputs:
    high: Series
    low: Series
    close: Series
    k_period: int (default 10)
    d_period: int (default 3)
    display_index: pandas.Index or None
Outputs:
    DataFrame: 'FastK', 'FastD'
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def stochastic_fast(
    high,
    low,
    close,
    k_period=10,
    d_period=3,
    display_index=None
):
    """
    Stochastic Fast
    Thinkscript: StochasticFast
    Params:
        high: pd.Series
        low: pd.Series
        close: pd.Series
        k_period: int
        d_period: int
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "FastK", "FastD"
    """
    hh = IndicatorUtils.highest(high, k_period)
    ll = IndicatorUtils.lowest(low, k_period)
    fastk = 100 * (close - ll) / (hh - ll)
    fastd = IndicatorUtils.simple_moving_avg(fastk, d_period)
    result = pd.DataFrame({
        "FastK": fastk,
        "FastD": fastd
    }, index=close.index)
    if display_index is not None:
        result = result.reindex(display_index, method='ffill')
    return result