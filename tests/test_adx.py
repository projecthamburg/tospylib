import pandas as pd
from tospylib.indicators.adx import adx

def test_adx():
    df = pd.DataFrame({'High': range(1, 41), 'Low': range(0, 40), 'Close': range(1, 41)})  # 40 bars of data
    result = adx(df)
    assert set(result.columns) == {"ADX", "DI+", "DI-"}
    assert len(result) == len(df)

def test_adx_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = adx(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"ADX", "+DI", "-DI"}
    assert len(result) == len(df)
