"""
Pivot Points
Thinkscript reference: PivotPoints (source not available)
Standard implementation based on daily/week/month OHLC
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
Inputs:
    high: Series
    low: Series
    close: Series
    timeframe: str ("DAY", "WEEK", "MONTH")
    display_index: pandas.Index or None
Outputs:
    DataFrame: R3, R2, R1, PP, S1, S2, S3
"""
import pandas as pd
import numpy as np

def pivot_points(high, low, close, timeframe="DAY", display_index=None):
    """
    Calculate standard pivot points based on timeframe OHLC data
    
    Parameters:
    -----------
    high : pd.Series or array-like
        High price series
    low : pd.Series or array-like
        Low price series
    close : pd.Series or array-like
        Close price series
    timeframe : str, optional
        Timeframe for pivot calculation ("DAY", "WEEK", "MONTH"), default "DAY"
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: R3, R2, R1, PP, S1, S2, S3
        
    Notes:
    ------
    - Handles NaN values in input by propagating them to output
    - Accepts various input types (lists, arrays, Series)
    - For non-numeric inputs, attempts to convert to numeric or propagates NaN
    - Verifies that timeframe is one of the valid options
    """
    # Validate timeframe first
    if timeframe not in {"DAY", "WEEK", "MONTH"}:
        raise ValueError("timeframe must be DAY, WEEK, or MONTH")
    
    # Convert inputs to Series if they aren't already
    try:
        high = pd.Series(high, dtype='float64')
    except (ValueError, TypeError):
        # Handle non-numeric inputs by trying to convert or creating NaN Series
        try:
            high = pd.Series(pd.to_numeric(high, errors='coerce'))
        except:
            # If all else fails, create a Series of NaNs with same length
            if hasattr(high, '__len__'):
                high = pd.Series([np.nan] * len(high))
            else:
                high = pd.Series([np.nan])
    
    try:
        low = pd.Series(low, dtype='float64')
    except (ValueError, TypeError):
        try:
            low = pd.Series(pd.to_numeric(low, errors='coerce'))
        except:
            if hasattr(low, '__len__'):
                low = pd.Series([np.nan] * len(low))
            else:
                low = pd.Series([np.nan])
    
    try:
        close = pd.Series(close, dtype='float64')
    except (ValueError, TypeError):
        try: 
            close = pd.Series(pd.to_numeric(close, errors='coerce'))
        except:
            if hasattr(close, '__len__'):
                close = pd.Series([np.nan] * len(close))
            else:
                close = pd.Series([np.nan])
    
    # Handle empty series case
    if len(high) == 0 or len(low) == 0 or len(close) == 0:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["R3", "R2", "R1", "PP", "S1", "S2", "S3"])
    
    # Create aligned series based on the index
    if not (high.index.equals(low.index) and high.index.equals(close.index)):
        # If indexes don't match, align them
        high, low, close = pd.concat([high, low, close], axis=1, join='outer').iloc[:, 0], \
                           pd.concat([high, low, close], axis=1, join='outer').iloc[:, 1], \
                           pd.concat([high, low, close], axis=1, join='outer').iloc[:, 2]
    
    # Calculate pivot points
    PP = (high + low + close) / 3
    R1 = (2 * PP) - low
    S1 = (2 * PP) - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = high + 2 * (PP - low)
    S3 = low - 2 * (high - PP)
    
    # Create result DataFrame
    pivots = pd.DataFrame({
        "R3": R3, "R2": R2, "R1": R1, "PP": PP, "S1": S1, "S2": S2, "S3": S3
    }, index=high.index)
    
    # Handle display_index
    if display_index is not None:
        if len(display_index) == 0:
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=pivots.columns, index=display_index)
            
        # Use a more robust approach for reindexing
        try:
            # Create a new DataFrame with the target index
            reindexed = pd.DataFrame(index=display_index, columns=pivots.columns)
            
            # Get common dates
            common_dates = sorted(set(pivots.index).intersection(set(display_index)))
            
            # Copy values for common dates
            if common_dates:
                for date in common_dates:
                    reindexed.loc[date] = pivots.loc[date]
            
            # Forward fill for dates not in common
            if len(pivots) > 0:
                # Convert indices to handle different types
                try:
                    pivots_idx = pd.Index(pivots.index)
                    display_idx = pd.Index(display_index)
                    
                    # For dates not in common
                    for date in display_idx.difference(common_dates):
                        try:
                            # Find closest previous date
                            mask = pivots_idx < date
                            if mask.any():
                                closest_idx = pivots_idx[mask].max()
                                reindexed.loc[date] = pivots.loc[closest_idx]
                        except:
                            # If comparison fails, use last row
                            if len(pivots) > 0:
                                reindexed.loc[date] = pivots.iloc[-1]
                except:
                    # Fallback: use standard reindex with ffill
                    pivots = pivots.reindex(display_index, method='ffill')
                    return pivots
            
            # Fill any remaining NaNs
            reindexed = reindexed.ffill()
            return reindexed
        except:
            # Fallback to the original simpler reindex method
            pivots = pivots.reindex(display_index, method='ffill')
    
    return pivots
