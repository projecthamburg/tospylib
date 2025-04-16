import pandas as pd
from tospylib.indicators.relative_strength import relative_strength

def test_relative_strength():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = relative_strength(df['Close'], length=3)
    assert len(result) == len(df)
    assert result.iloc[-1] > 0  # Should be positive

def test_relative_strength_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = relative_strength(df['Close'], length=14)
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)
