"""
StochasticFast Indicator
Thinkscript formula reference: StochasticFast
Inputs: input over_bought=80; input over_sold=20; input KPeriod=10; input DPeriod=3; input priceH=high; input priceL=low; input priceC=close; input averageType=AverageType.SIMPLE; input showBreakoutSignals={...};
For explicit Thinkscript parameter definitions, see reserved_words.md.
"""
import pandas as pd
import numpy as np

def stochastic_fast(high, low, close, k_period=10, d_period=3, displace=0, display_index=None):
    """
    Stochastic Fast Oscillator, Thinkscript-style.
    
    Parameters:
    -----------
    high : pd.Series
        High price series
    low : pd.Series
        Low price series
    close : pd.Series
        Close price series
    k_period : int, optional
        Period for %K calculation, default 10
    d_period : int, optional
        Period for %D calculation, default 3
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns:
        - K: Fast stochastic %K
        - D: Fast stochastic %D
    """
    high_shifted = pd.Series(high).shift(-displace)
    low_shifted = pd.Series(low).shift(-displace)
    close_shifted = pd.Series(close).shift(-displace)
    
    # Calculate %K
    lowest_low = low_shifted.rolling(k_period, min_periods=1).min()
    highest_high = high_shifted.rolling(k_period, min_periods=1).max()
    k = 100 * ((close_shifted - lowest_low) / (highest_high - lowest_low))
    
    # Calculate %D
    d = k.rolling(d_period, min_periods=1).mean()
    
    if display_index is not None:
        k = k.reindex(display_index, method="ffill")
        d = d.reindex(display_index, method="ffill")
    
    return pd.DataFrame({
        'K': k,
        'D': d
    })
