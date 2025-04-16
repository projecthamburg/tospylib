import pandas as pd
from tospylib.indicators.relative_strength import relative_strength

def test_relative_strength():
    df = pd.DataFrame({'Close': range(1, 41)})  # 40 bars of data
    result = relative_strength(df['Close'], length=14)
    assert set(result.columns) == {"Value"}
    assert len(result) == len(df)

def test_relative_strength_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = relative_strength(df['Close'], length=14)
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)
