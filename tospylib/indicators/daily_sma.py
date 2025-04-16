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
    Robust Daily SMA, broadcast by calendar date!
    """
    # Compute rolling on daily
    daily_sma_series = calculation_df[price_type].rolling(window=length, min_periods=1).mean()
    daily_sma_map = pd.Series(daily_sma_series.values, index=calculation_df.index.date)
    # Map every minute/bar by .date, not full datetime
    minute_to_date = display_df.index.date
    mapped = pd.Series(daily_sma_map.loc[minute_to_date].values, index=display_df.index)
    if show_only_last_period:
        # only mark SMA at last bar of each day
        last_per_day = display_df.groupby(minute_to_date).tail(1).index
        mapped[~mapped.index.isin(last_per_day)] = float("nan")
    return mapped