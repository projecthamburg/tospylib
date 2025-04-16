"""
Bollinger Bands
Thinkscript reference: BollingerBands
Inputs:
    price: Series
    length: int (default 20)
    num_dev_dn: float (default -2.0)
    num_dev_up: float (default 2.0)
    display_index: pandas.Index or None
Outputs:
    DataFrame: 'MidLine', 'LowerBand', 'UpperBand'
"""
import pandas as pd
from ..indicator_utils import IndicatorUtils

def bollinger_bands(
    price,
    length=20,
    num_dev_dn=-2.0,
    num_dev_up=2.0,
    display_index=None
):
    """
    Bollinger Bands
    Thinkscript: BollingerBands
    Params:
        price: pd.Series
        length: int
        num_dev_dn: float (num standard deviations for lower band)
        num_dev_up: float (num standard deviations for upper band)
        display_index: pandas.Index or None
    Returns:
        pd.DataFrame with columns "MidLine", "LowerBand", "UpperBand"
    """
    mid = IndicatorUtils.simple_moving_avg(price, length)
    sd = IndicatorUtils.stdev(price, length)
    lower = mid + num_dev_dn * sd
    upper = mid + num_dev_up * sd
    result = pd.DataFrame({
        "MidLine": mid,
        "LowerBand": lower,
        "UpperBand": upper
    }, index=price.index)
    if display_index is not None:
        result = result.reindex(display_index, method='ffill')
    return result
