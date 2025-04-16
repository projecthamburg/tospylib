import pandas as pd
from tospylib.indicators.macd import macd

def test_macd():
    # TODO: add unit test for macd
    assert True  # Placeholder

def test_macd_length():
    df = pd.DataFrame({'Close': range(1,41)})  # 40 bars of data
    result = macd(df['Close'])
    assert set(result.columns) == {"Value","Avg","Diff"}
    assert len(result) == len(df)
