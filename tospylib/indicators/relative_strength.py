"""
RelativeStrength Indicator
Thinkscript formula reference: RelativeStrength
Inputs: input CorrelationWithSecurity="SPX";
For explicit Thinkscript parameter definitions, see ../reserved_words.md.
"""
import pandas as pd
import numpy as np

def relative_strength(price, length=14, displace=0, display_index=None):
    """
    Relative Strength Index (RSI), Thinkscript-style.
    
    Parameters:
    -----------
    price : pd.Series
        Price series to calculate RSI on
    length : int, optional
        Periods for RSI calculation, default 14
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.Series
        RSI values between 0 and 100
    """
    price_shifted = pd.Series(price).shift(-displace)
    delta = price_shifted.diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(length, min_periods=1).mean()
    avg_loss = loss.rolling(length, min_periods=1).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    if display_index is not None:
        rsi = rsi.reindex(display_index, method="ffill")
    
    return rsi
