import pandas as pd
from tospylib.indicators.simple_moving_avg import simple_moving_avg

def test_simple_moving_avg():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = simple_moving_avg(df['Close'], length=3)
    assert round(result.iloc[-1],5) == 9.0  # Last three: 8,9,10
