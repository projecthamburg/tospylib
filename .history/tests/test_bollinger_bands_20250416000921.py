import pandas as pd
from tospylib.indicators.bollinger_bands import bollinger_bands

def test_bollinger_bands_smoke():
    s = pd.Series(range(1,22))
    result = bollinger_bands(s, length=5)
    assert set(result.columns) == {"MidLine", "LowerBand", "UpperBand"}
    assert len(result) == len(s)
