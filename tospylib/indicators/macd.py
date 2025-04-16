"""
MACD Indicator
Thinkscript formula reference: MACD
Inputs: input fastLength=12; input slowLength=26; input MACDLength=9; input averageType=AverageType.EXPONENTIAL; input showBreakoutSignals=no;
For explicit Thinkscript parameter definitions, see reserved_words.md.
"""
import pandas as pd
import numpy as np

def macd(series, fast_length=12, slow_length=26, signal_length=9):
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Parameters:
    -----------
    series : pd.Series
        Price series to calculate MACD on
    fast_length : int, optional
        Fast EMA period, default 12
    slow_length : int, optional
        Slow EMA period, default 26
    signal_length : int, optional
        Signal line period, default 9
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns:
        - Value: MACD line (fast EMA - slow EMA)
        - Avg: Signal line (EMA of MACD line)
        - Diff: MACD histogram (MACD line - Signal line)
    """
    # Calculate fast and slow EMAs
    fast_ema = series.ewm(span=fast_length, adjust=False).mean()
    slow_ema = series.ewm(span=slow_length, adjust=False).mean()
    
    # Calculate MACD line
    macd_line = fast_ema - slow_ema
    
    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_length, adjust=False).mean()
    
    # Calculate MACD histogram
    histogram = macd_line - signal_line
    
    # Create DataFrame with results
    result = pd.DataFrame({
        'Value': macd_line,
        'Avg': signal_line,
        'Diff': histogram
    })
    
    return result
