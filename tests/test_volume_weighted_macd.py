import pandas as pd
from tospylib.indicators.volume_weighted_macd import volume_weighted_macd

def test_volume_weighted_macd():
    df = pd.DataFrame({
        'Close': range(1,41),
        'Volume': [100] * 40
    })
    result = volume_weighted_macd(df['Close'], df['Volume'])
    assert set(result.columns) == {"Value","Avg","Diff"}
    assert len(result) == len(df)
