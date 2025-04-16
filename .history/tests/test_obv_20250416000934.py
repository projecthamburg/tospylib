import pandas as pd
from tospylib.indicators.obv import obv

def test_obv():
    df = pd.DataFrame({'Close': range(1,41), 'Volume': range(1,41)})  # 40 bars of data
    result = obv(df['Close'], df['Volume'])
    assert set(result.columns) == {"Value"}
    assert len(result) == len(df)

def test_obv_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = obv(df['Close'], df['Volume'])
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)
