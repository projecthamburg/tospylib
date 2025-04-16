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
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
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
    
    if display_index is not None:
        adx = adx.reindex(display_index, method="ffill")
        plus_di = plus_di.reindex(display_index, method="ffill")
        minus_di = minus_di.reindex(display_index, method="ffill")
    
    return pd.DataFrame({
        'ADX': adx,
        '+DI': plus_di,
        '-DI': minus_di
    })
