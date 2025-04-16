import pandas as pd
from tospylib.indicators.stochastic_fast import stochastic_fast

def test_stochastic_fast_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = stochastic_fast(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"K", "D"}
    assert len(result) == len(df)
