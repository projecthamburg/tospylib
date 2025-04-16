import pandas as pd
from tospylib.indicators.mov_avg_exponential import mov_avg_exponential

def test_mov_avg_exponential():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = mov_avg_exponential(df['Close'], length=3)
    assert len(result) == len(df)
    assert result.iloc[-1] > 0  # Should be positive
