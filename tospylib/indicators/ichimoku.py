"""
Ichimoku Kinko Hyo
Thinkcript reference: Ichimoku
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
Inputs:
    high: Series
    low: Series
    close: Series
    tenkan_period: int (default 9)
    kijun_period: int (default 26)
    display_index: pandas.Index or None
Outputs:
    DataFrame: Tenkan, Kijun, SenkouA, SenkouB, Chikou
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def ichimoku(high, low, close, tenkan_period=9, kijun_period=26, display_index=None):
    tenkan = (IndicatorUtils.highest(high, tenkan_period) + IndicatorUtils.lowest(low, tenkan_period)) / 2
    kijun  = (IndicatorUtils.highest(high, kijun_period) + IndicatorUtils.lowest(low, kijun_period)) / 2
    senkou_a = ((tenkan + kijun) / 2).shift(kijun_period)
    senkou_b = (
        (IndicatorUtils.highest(high.shift(kijun_period), 2 * kijun_period) +
         IndicatorUtils.lowest(low.shift(kijun_period), 2 * kijun_period)) / 2
    )
    chikou = close.shift(-kijun_period)
    ichimoku_df = pd.DataFrame({
        "Tenkan": tenkan,
        "Kijun": kijun,
        "SenkouA": senkou_a,
        "SenkouB": senkou_b,
        "Chikou": chikou,
    }, index=close.index)
    
    # Handle display_index if provided
    if display_index is not None:
        if len(display_index) == 0:  # Handle empty index case
            return pd.DataFrame(index=display_index, columns=ichimoku_df.columns)
        
        # Create a new dataframe with the target index
        reindexed = pd.DataFrame(index=display_index, columns=ichimoku_df.columns)
        
        # Get the common dates between original and new index
        common_dates = sorted(set(ichimoku_df.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = ichimoku_df.loc[date].astype(float)
        
        # Forward fill for dates in display_index not in original index
        if len(ichimoku_df) > 0:  # Only if we have data
            # Convert indices to pandas indexes if they're not already
            df_idx = pd.Index(ichimoku_df.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                # Find the closest previous date
                try:
                    mask = df_idx < date
                    if mask.any():
                        closest_idx = df_idx[mask].max()
                        reindexed.loc[date] = ichimoku_df.loc[closest_idx].astype(float)
                except:
                    # If comparison fails, use last row as fallback
                    if len(ichimoku_df) > 0:
                        reindexed.loc[date] = ichimoku_df.iloc[-1].astype(float)
        
        # Fill any remaining NaN values
        reindexed = reindexed.ffill()
        return reindexed
    
    return ichimoku_df