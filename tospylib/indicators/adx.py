"""
ADX Indicator
Thinkscript formula reference: ADX
Inputs: input length=14; input averageType=AverageType.WILDERS;
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd
import numpy as np

def adx(high, low, close, length=14, displace=0, display_index=None):
    """
    Average Directional Index (ADX), Thinkscript-style.
    
    Parameters:
    -----------
    high : pd.Series
        High price series
    low : pd.Series
        Low price series
    close : pd.Series
        Close price series
    length : int, optional
        Period for ADX calculation, default 14
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns:
        - ADX: Average Directional Index
        - +DI: Plus Directional Indicator
        - -DI: Minus Directional Indicator
    """
    # Convert inputs to Series if they aren't already
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    
    # Shift data if needed
    high_shifted = high.shift(-displace)
    low_shifted = low.shift(-displace)
    close_shifted = close.shift(-displace)
    
    # Calculate True Range
    tr1 = high_shifted - low_shifted
    tr2 = abs(high_shifted - close_shifted.shift(1))
    tr3 = abs(low_shifted - close_shifted.shift(1))
    
    # Fix: Use numpy nanmax to handle NaN and -inf values
    df_tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3})
    tr = df_tr.apply(lambda x: max(x.fillna(0)), axis=1)
    
    # Calculate Directional Movement
    up_move = high_shifted - high_shifted.shift(1)
    down_move = low_shifted.shift(1) - low_shifted
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Calculate Wilder's Smoothing
    tr_smooth = tr.ewm(span=length, adjust=False).mean()
    plus_di = 100 * pd.Series(plus_dm).ewm(span=length, adjust=False).mean() / tr_smooth
    minus_di = 100 * pd.Series(minus_dm).ewm(span=length, adjust=False).mean() / tr_smooth
    
    # Calculate ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.ewm(span=length, adjust=False).mean()
    
    # Handle NaN values
    adx = adx.fillna(0)
    plus_di = plus_di.fillna(0)
    minus_di = minus_di.fillna(0)
    
    # Create the result DataFrame
    result = pd.DataFrame({
        'ADX': adx,
        '+DI': plus_di,
        '-DI': minus_di
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
                reindexed.loc[date] = result.loc[date]
        
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
                        reindexed.loc[date] = result.iloc[-1]
                else:
                    # For matching types, try to find the closest date
                    try:
                        mask = result_idx < date
                        if mask.any():
                            closest_idx = result_idx[mask].max()
                            reindexed.loc[date] = result.loc[closest_idx]
                    except:
                        # If comparison fails, use last row as fallback
                        if len(result) > 0:
                            reindexed.loc[date] = result.iloc[-1]
        
        # Fill any remaining NaN values with the last known value
        reindexed = reindexed.ffill().fillna(0)
        return reindexed
    
    return result
