"""
Daily SMA (multi-timeframe support)
Thinkscript reference: DailySMA
Inputs:
    calculation_df: DataFrame (should be at daily agg, e.g. from resample)
    display_df: DataFrame (can be intraday or any period)
    price_type: str ("Close", "Open", etc.)
    length: int
    displace: int
    show_only_last_period: bool (default False)
Output:
    Series aligned to display_df
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def daily_sma(
    calculation_df,
    display_df,
    price_type="Close",
    length=9,
    displace=0,
    show_only_last_period=False
):
    """
    Daily Simple Moving Average (multi-timeframe broadcast)
    Thinkscript: DailySMA
    Params:
        calculation_df: pd.DataFrame (daily OHLCV)
        display_df: pd.DataFrame (minute/daily for display)
        price_type: str ("Close", etc.)
        length: int
        displace: int
        show_only_last_period: bool
    Returns:
        pd.Series (broadcast to display_df.index)
    """
    price = calculation_df[price_type].shift(-displace)
    sma = IndicatorUtils.simple_moving_avg(price, length)
    # Only show last period's value if requested
    if show_only_last_period:
        out = pd.Series(index=display_df.index, dtype=float)
        out[:] = float("nan")
        if not pd.isna(sma.iloc[-1]):
            out.iloc[-1] = sma.iloc[-1]
        return out
    # Broadcast to all of display_df
    return sma.reindex(display_df.index, method='ffill')
