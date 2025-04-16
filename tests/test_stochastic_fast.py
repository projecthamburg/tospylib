import pandas as pd
from tospylib.indicators.stochastic_fast import stochastic_fast

def test_stochastic_fast():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = stochastic_fast(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"K","D"}
    assert len(result) == len(df)
    assert (result['K'] >= 0).all() and (result['K'] <= 100).all()
