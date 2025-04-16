import pandas as pd
from tospylib.indicators.ichimoku import ichimoku

def test_ichimoku():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = ichimoku(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"Tenkan","Kijun","SenkouA","SenkouB","Chikou"}
    assert len(result) == len(df)
