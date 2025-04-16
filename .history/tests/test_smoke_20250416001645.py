import pandas as pd
from tospylib.indicators.macd import macd

def test_smoke():
    idx = pd.date_range("2024-06-01", periods=100)
    series = pd.Series(range(100), index=idx)
    macd_out = macd(series)
    assert not macd_out.isnull().all().all() 