"""
Relative Strength Indicator
Thinkscript reference: RelativeStrength
Inputs:
    price: Series (the primary/security)
    benchmark_price: Series (comparison security, e.g., SPX)
    display_index: pandas.Index or None
Outputs:
    Series (RS: price / benchmark_price), broadcast to display_index if provided

Behaves like: plot RS = if close2 == 0 then 0 else close/close2;
"""
import pandas as pd
import numpy as np

def relative_strength(
    price,
    benchmark_price,
    display_index=None
):
    """
    Relative Strength (price vs benchmark)
    Thinkscript: RelativeStrength
    Params:
        price: pd.Series
        benchmark_price: pd.Series
        display_index: pandas.Index or None
    Returns:
        pd.Series
    """
    # Convert inputs to Series if they aren't already
    price = pd.Series(price)
    benchmark_price = pd.Series(benchmark_price)
    
    # Handle division by zero by replacing zeros with NaN
    rs = price / benchmark_price.replace(0, np.nan)
    
    # Replace NaN values with zeros
    rs = rs.fillna(0)
    
    # Reindex to display_index if provided (for multi-timeframe support)
    if display_index is not None:
        rs = rs.reindex(display_index, method="ffill")
        
    return rs
