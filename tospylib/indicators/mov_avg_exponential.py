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
    if display_index is not None:
        ema = ema.reindex(display_index, method="ffill")
    return ema
