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
    
    # Handle display_index if provided
    if display_index is not None:
        if len(display_index) == 0:  # Handle empty index case
            return pd.DataFrame(index=display_index, columns=result.columns)
        
        # Create a new dataframe with the target index
        reindexed = pd.DataFrame(index=display_index, columns=result.columns)
        
        # Get the common dates between original and new index
        common_dates = sorted(set(result.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = result.loc[date].astype(float)
        
        # Forward fill for dates in display_index not in original index
        if len(result) > 0:  # Only if we have data
            # Convert indices to pandas indexes if they're not already
            result_idx = pd.Index(result.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                # Find the closest previous date
                try:
                    mask = result_idx < date
                    if mask.any():
                        closest_idx = result_idx[mask].max()
                        reindexed.loc[date] = result.loc[closest_idx].astype(float)
                except:
                    # If comparison fails, use last row as fallback
                    if len(result) > 0:
                        reindexed.loc[date] = result.iloc[-1].astype(float)
        
        # Fill any remaining NaN values
        reindexed = reindexed.ffill().fillna(0)
        return reindexed
    
    return result
