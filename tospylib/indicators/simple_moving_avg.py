"""
SimpleMovingAvg Indicator
Thinkscript formula reference: SimpleMovingAvg
Inputs: input price=close; input length=9; input displace=0; input showBreakoutSignals=no;
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd

def simple_moving_avg(price, length=9, displace=0, display_index=None):
    """
    Simple Moving Average (SMA), Thinkscript-style.
    price: pandas Series of prices
    length: int, periods for moving average
    displace: int, offset, Thinkscript style (negative=look back, positive=look forward)
    display_index: optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    """
    price_shifted = pd.Series(price).shift(-displace)
    sma = price_shifted.rolling(length, min_periods=1).mean()
    
    # Handle display_index if provided
    if display_index is not None:
        if len(display_index) == 0:  # Handle empty index case
            return pd.Series(index=display_index)
        
        # Create a new series with the target index
        reindexed = pd.Series(index=display_index)
        
        # Get the common dates between original and new index
        common_dates = sorted(set(sma.index).intersection(set(display_index)))
        
        # Copy values for common dates
        if common_dates:
            for date in common_dates:
                reindexed.loc[date] = float(sma.loc[date])
        
        # Handle dates in display_index not in original index
        if len(sma) > 0:  # Only if we have data
            # Convert indices to pandas indexes if they're not already
            sma_idx = pd.Index(sma.index)
            display_idx = pd.Index(display_index)
            
            # For dates not in common
            for date in display_idx.difference(common_dates):
                if isinstance(date, pd.Timestamp) and sma_idx.dtype != 'datetime64[ns]':
                    # Handle different index types
                    if len(sma) > 0:
                        reindexed.loc[date] = float(sma.iloc[-1])
                else:
                    # For matching types, try to find the closest date
                    try:
                        mask = sma_idx < date
                        if mask.any():
                            closest_idx = sma_idx[mask].max()
                            reindexed.loc[date] = float(sma.loc[closest_idx])
                    except:
                        # If comparison fails, use last value as fallback
                        if len(sma) > 0:
                            reindexed.loc[date] = float(sma.iloc[-1])
        
        # Fill any remaining NaN values
        reindexed = reindexed.ffill().fillna(0)
        return reindexed
    
    return sma
