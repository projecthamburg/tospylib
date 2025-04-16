"""
On-Balance Volume (OBV)
Thinkscript reference: OBV
Inputs:
    close: Series
    volume: Series
    display_index: pandas.Index or None
Outputs:
    Series: OBV values
"""
import pandas as pd
import numpy as np

def obv(
    close,
    volume,
    display_index=None
):
    """
    On-Balance Volume (OBV)
    Thinkscript: OBV
    Params:
        close: pd.Series
        volume: pd.Series
        display_index: pandas.Index or None
    Returns:
        pd.Series
    """
    obv = [0]
    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i-1]:
            obv.append(obv[-1] + volume.iloc[i])
        elif close.iloc[i] < close.iloc[i-1]:
            obv.append(obv[-1] - volume.iloc[i])
        else:
            obv.append(obv[-1])
    obv_series = pd.Series(obv, index=close.index)
    if display_index is not None:
        obv_series = obv_series.reindex(display_index, method="ffill")
    return obv_series