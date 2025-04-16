"""
BollingerBands Indicator
Thinkscript formula reference: BollingerBands
Inputs: input price=close; input displace=0; input length=20; input Num_Dev_Dn=-2.0; input Num_Dev_up=2.0; input averageType=AverageType.Simple;
For explicit Thinkscript parameter definitions, see reserved_words.md.
"""
import pandas as pd
import numpy as np

def bollinger_bands(price, length=20, displace=0, num_dev_dn=-2.0, num_dev_up=2.0, display_index=None):
    """
    Bollinger Bands, Thinkscript-style.
    
    Parameters:
    -----------
    price : pd.Series
        Price series to calculate bands on
    length : int, optional
        Periods for moving average, default 20
    displace : int, optional
        Offset, Thinkscript style (negative=look back, positive=look forward), default 0
    num_dev_dn : float, optional
        Number of standard deviations for lower band, default -2.0
    num_dev_up : float, optional
        Number of standard deviations for upper band, default 2.0
    display_index : pd.Index, optional
        Optionally reindex/ffill to another index (e.g., for multi-timeframe charts)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns:
        - MidLine: Simple moving average
        - LowerBand: MidLine + (num_dev_dn * standard deviation)
        - UpperBand: MidLine + (num_dev_up * standard deviation)
    """
    price_shifted = pd.Series(price).shift(-displace)
    midline = price_shifted.rolling(length, min_periods=1).mean()
    std = price_shifted.rolling(length, min_periods=1).std()
    
    lower_band = midline + (num_dev_dn * std)
    upper_band = midline + (num_dev_up * std)
    
    if display_index is not None:
        midline = midline.reindex(display_index, method="ffill")
        lower_band = lower_band.reindex(display_index, method="ffill")
        upper_band = upper_band.reindex(display_index, method="ffill")
    
    return pd.DataFrame({
        'MidLine': midline,
        'LowerBand': lower_band,
        'UpperBand': upper_band
    })
