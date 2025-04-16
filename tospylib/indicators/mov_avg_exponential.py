"""
MovAvgExponential Indicator
Thinkscript formula reference: MovAvgExponential
Inputs: input price=close; input length=9; input displace=0; input showBreakoutSignals=no;
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd

def mov_avg_exponential(price, length=9, displace=0, display_index=None):
    """
    Exponential Moving Average (EMA), Thinkscript-style.
    
    Parameters:
    -----------
    price : pd.Series
        Price series to calculate EMA on
    length : int, optional
        Periods for moving average, default 9
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.Series
        Exponential moving average series
    """
    price_shifted = pd.Series(price).shift(-displace)
    ema = price_shifted.ewm(span=length, adjust=False).mean()
    
    # Handle display_index if provided
    if display_index is not None:
        if len(display_index) == 0:  # Handle empty index case
            return pd.Series(index=display_index)
        
        # Create a new series with the target index
        reindexed = pd.Series(index=display_index)
        
        # Get the common dates between original and new index
        common_dates = sorted(set(ema.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = float(ema.loc[date])
        
        # Handle dates in display_index not in original index
        if len(ema) > 0:  # Only if we have data
            # Convert indices to pandas indexes if they're not already
            ema_idx = pd.Index(ema.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                # Find the closest previous date
                try:
                    mask = ema_idx < date
                    if mask.any():
                        closest_idx = ema_idx[mask].max()
                        reindexed.loc[date] = float(ema.loc[closest_idx])
                except:
                    # If comparison fails, use last value as fallback
                    if len(ema) > 0:
                        reindexed.loc[date] = float(ema.iloc[-1])
        
        # Fill any remaining NaN values
        reindexed = reindexed.ffill().fillna(0)
        return reindexed
    
    return ema
