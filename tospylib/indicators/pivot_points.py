"""
Pivot Points
Thinkscript reference: PivotPoints (source not available)
Standard implementation based on daily/week/month OHLC
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
    # This is a standard implementation for classic Pivot Points
    if timeframe not in {"DAY", "WEEK", "MONTH"}:
        raise ValueError("timeframe must be DAY, WEEK, or MONTH")
    resample_rule = {"DAY": "1D", "WEEK": "1W", "MONTH": "1M"}[timeframe]
    resampled = pd.DataFrame({
        "High": high.resample(resample_rule).max(),
        "Low": low.resample(resample_rule).min(),
        "Close": close.resample(resample_rule).last(),
    })
    PP = (resampled["High"] + resampled["Low"] + resampled["Close"]) / 3
    R1 = 2*PP - resampled["Low"]
    S1 = 2*PP - resampled["High"]
    R2 = PP + (resampled["High"] - resampled["Low"])
    S2 = PP - (resampled["High"] - resampled["Low"])
    R3 = resampled["High"] + 2*(PP - resampled["Low"])
    S3 = resampled["Low"] - 2*(resampled["High"] - PP)
    pivots = pd.DataFrame({
        "R3": R3, "R2": R2, "R1": R1, "PP": PP, "S1": S1, "S2": S2, "S3": S3
    }, index=PP.index)
    # Broadcast to line up with original (display) index
    if display_index is not None:
        pivots = pivots.reindex(display_index, method='ffill')
    return pivots
