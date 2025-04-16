import pandas as pd
from tospylib.indicators.adx import adx

def test_adx():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = adx(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"ADX","DI+","DI-"}
    assert len(result) == len(df)
    assert (result['ADX'] >= 0).all() and (result['ADX'] <= 100).all()

def test_adx_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = adx(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"ADX", "+DI", "-DI"}
    assert len(result) == len(df)
