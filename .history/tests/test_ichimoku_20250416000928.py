import pandas as pd
from tospylib.indicators.ichimoku import ichimoku

def test_ichimoku_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = ichimoku(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"Tenkan", "Kijun", "SenkouA", "SenkouB", "Chikou"}
    assert len(result) == len(df)
