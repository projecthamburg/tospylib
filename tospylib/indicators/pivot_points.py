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
    high : pd.Series
        High price series
    low : pd.Series
        Low price series
    close : pd.Series
        Close price series
    timeframe : str, optional
        Timeframe for pivot calculation ("DAY", "WEEK", "MONTH"), default "DAY"
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: R3, R2, R1, PP, S1, S2, S3
    """
    # Convert inputs to Series if they aren't already
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    
    # This is a standard implementation for classic Pivot Points
    if timeframe not in {"DAY", "WEEK", "MONTH"}:
        raise ValueError("timeframe must be DAY, WEEK, or MONTH")
    
    # Calculate pivot points directly without resampling
    PP = (high + low + close) / 3
    R1 = 2*PP - low
    S1 = 2*PP - high
    R2 = PP + (high - low)
    S2 = PP - (high - low)
    R3 = high + 2*(PP - low)
    S3 = low - 2*(high - PP)
    
    pivots = pd.DataFrame({
        "R3": R3, "R2": R2, "R1": R1, "PP": PP, "S1": S1, "S2": S2, "S3": S3
    }, index=close.index)
    
    # Broadcast to line up with original (display) index
    if display_index is not None:
        pivots = pivots.reindex(display_index, method='ffill')
    
    return pivots
