import pandas as pd
from tospylib.indicators.pivot_points import pivot_points

def test_pivot_points_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = pivot_points(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"PP", "R1", "R2", "R3", "S1", "S2", "S3"}
    assert len(result) == len(df)