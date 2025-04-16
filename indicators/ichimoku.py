"""
Ichimoku Kinko Hyo
Thinkscript reference: Ichimoku
Inputs:
    high: Series
    low: Series
    close: Series
    tenkan_period: int (default 9)
    kijun_period: int (default 26)
    display_index: pandas.Index or None
Outputs:
    DataFrame: Tenkan, Kijun, SpanA, SpanB, Chikou
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def ichimoku(
    high,
    low,
    close,
    tenkan_period=9,
    kijun_period=26,
    display_index=None
):
    """
    Ichimoku Kinko Hyo
    Thinkscript: Ichimoku
    Params:
        high: pd.Series
        low: pd.Series
        close: pd.Series
        tenkan_period: int
        kijun_period: int
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "Tenkan", "Kijun", "SpanA", "SpanB", "Chikou"
    """
    tenkan = (IndicatorUtils.highest(high, tenkan_period) + IndicatorUtils.lowest(low, tenkan_period)) / 2
    kijun  = (IndicatorUtils.highest(high, kijun_period) + IndicatorUtils.lowest(low, kijun_period)) / 2
    span_a = ((tenkan + kijun) / 2).shift(kijun_period)
    span_b = (
        (IndicatorUtils.highest(high.shift(kijun_period), 2 * kijun_period) +
         IndicatorUtils.lowest(low.shift(kijun_period), 2 * kijun_period)) / 2
    )
    chikou = close.shift(-kijun_period)
    ichimoku_df = pd.DataFrame({
        "Tenkan": tenkan,
        "Kijun": kijun,
        "SpanA": span_a,
        "SpanB": span_b,
        "Chikou": chikou,
    }, index=close.index)
    if display_index is not None:
        ichimoku_df = ichimoku_df.reindex(display_index, method='ffill')
    return ichimoku_df