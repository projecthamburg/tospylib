import pandas as pd
from tospylib.indicators.obv import obv

def test_obv():
    df = pd.DataFrame({
        'Close': [10, 11, 10, 12, 11],
        'Volume': [100, 200, 150, 300, 250]
    })
    result = obv(df['Close'], df['Volume'])
    assert len(result) == len(df)
    assert result.iloc[-1] != 0  # Should have some value

def test_obv_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = obv(df['Close'], df['Volume'])
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)
