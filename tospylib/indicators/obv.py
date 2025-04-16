"""
On-Balance Volume (OBV)
Thinkscript reference: OBV
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
Inputs:
    close: Series
    volume: Series
    display_index: pandas.Index or None
Outputs:
    Series: OBV values
"""
import pandas as pd
import numpy as np

def obv(close, volume, display_index=None):
    """
    Calculate On-Balance Volume (OBV)
    
    Parameters:
    -----------
    close : pd.Series
        Close price series
    volume : pd.Series
        Volume series
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.Series
        On-Balance Volume values
    
    Notes:
    ------
    - Handles NaN values by propagating them (NaN in either input results in NaN in output)
    - Both input series should have the same length
    - For best results, inputs should be aligned by index
    """
    # Convert inputs to Series if they aren't already
    close = pd.Series(close)
    volume = pd.Series(volume)
    
    # Check for empty series
    if len(close) == 0 or len(volume) == 0:
        return pd.Series([], index=close.index)
    
    # Create aligned series based on the index
    if not close.index.equals(volume.index):
        # If indexes don't match, align them
        close, volume = close.align(volume, join='outer')
    
    # Initialize OBV series
    obv_values = pd.Series(0, index=close.index)
    
    # Handle edge case: single-element series
    if len(close) == 1:
        return obv_values
    
    # Calculate OBV
    for i in range(1, len(close)):
        # Skip calculation if either current or previous close/volume has NaN
        if (pd.isna(close.iloc[i]) or pd.isna(close.iloc[i-1]) or 
            pd.isna(volume.iloc[i])):
            obv_values.iloc[i] = np.nan
        else:
            if close.iloc[i] > close.iloc[i-1]:
                obv_values.iloc[i] = obv_values.iloc[i-1] + volume.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv_values.iloc[i] = obv_values.iloc[i-1] - volume.iloc[i]
            else:
                obv_values.iloc[i] = obv_values.iloc[i-1]
    
    # Handle display_index
    if display_index is not None:
        # Use more robust reindexing approach
        if len(display_index) == 0:
            return pd.Series(index=display_index)
            
        # Create new series with target index
        reindexed = pd.Series(index=display_index)
        
        # Get common dates
        common_dates = sorted(set(obv_values.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = obv_values.loc[date]
        
        # Handle forward filling
        if len(obv_values) > 0:
            # Convert indices to pandas indexes
            orig_idx = pd.Index(obv_values.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                try:
                    # Find closest previous date
                    mask = orig_idx < date
                    if mask.any():
                        closest_idx = orig_idx[mask].max()
                        reindexed.loc[date] = obv_values.loc[closest_idx]
                except:
                    # If comparison fails, use last value
                    if not obv_values.isna().all():
                        reindexed.loc[date] = obv_values.iloc[-1]
        
        # Fill remaining NaNs
        obv_values = reindexed.ffill()
        
    return obv_values
