"""
BollingerBands Indicator
Thinkscript formula reference: BollingerBands
Inputs: input price=close; input displace=0; input length=20; input Num_Dev_Dn=-2.0; input Num_Dev_up=2.0; input averageType=AverageType.Simple;
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd
import numpy as np

def bollinger_bands(price, length=20, displace=0, num_dev_dn=-2.0, num_dev_up=2.0, display_index=None):
    """
    Bollinger Bands, Thinkscript-style.
    
    Parameters:
    -----------
    price : pd.Series
        Price series to calculate bands on
    length : int, optional
        Periods for moving average, default 20
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    num_dev_dn : float, optional
        Number of standard deviations for lower band, default -2.0
    num_dev_up : float, optional
        Number of standard deviations for upper band, default 2.0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns:
        - MidLine: Simple moving average
        - LowerBand: MidLine + (num_dev_dn * standard deviation)
        - UpperBand: MidLine + (num_dev_up * standard deviation)
    """
    price_shifted = pd.Series(price).shift(-displace)
    midline = price_shifted.rolling(length, min_periods=1).mean()
    std = price_shifted.rolling(length, min_periods=1).std()
    
    lower_band = midline + (num_dev_dn * std)
    upper_band = midline + (num_dev_up * std)
    
    # Create result DataFrame
    result = pd.DataFrame({
        'MidLine': midline,
        'LowerBand': lower_band,
        'UpperBand': upper_band
    })
    
    # Handle display_index if provided
    if display_index is not None:
        if len(display_index) == 0:  # Handle empty index case
            return pd.DataFrame(index=display_index, columns=result.columns)
        
        # Create a new dataframe with the target index and fill with NaN
        reindexed = pd.DataFrame(index=display_index, columns=result.columns)
        
        # Get the common dates between original and new index
        common_dates = sorted(set(result.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = result.loc[date].astype(float)
        
        # Forward fill for dates in display_index not in original index
        # Instead of comparing dates directly, we'll use index position logic
        if len(result) > 0:  # Only if we have data
            # Convert indices to pandas indexes if they're not already
            result_idx = pd.Index(result.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                # Find the closest previous date in the original index
                # that is less than the current date
                if isinstance(date, pd.Timestamp) and result_idx.dtype != 'datetime64[ns]':
                    # Handle the case where the indices have different types
                    # This is a simplified approach - for mixed index types,
                    # we'll just use the last value from the original result
                    if len(result) > 0:
                        reindexed.loc[date] = result.iloc[-1].astype(float)
                else:
                    # For matching types, try to find the closest date
                    try:
                        mask = result_idx < date
                        if mask.any():
                            closest_idx = result_idx[mask].max()
                            reindexed.loc[date] = result.loc[closest_idx].astype(float)
                    except:
                        # If comparison fails, use last row as fallback
                        if len(result) > 0:
                            reindexed.loc[date] = result.iloc[-1].astype(float)
        
        # Fill any remaining NaN values with the last known value
        reindexed = reindexed.ffill().fillna(0)
        return reindexed
    
    return result
