import pandas as pd
from tospylib.indicators.daily_sma import daily_sma

def test_daily_sma_minute_to_daily():
    idx = pd.date_range("2024-06-01", periods=3, freq="D")
    daily = pd.DataFrame({'Close':[10, 20, 30]}, index=idx)
    # Each 4-minute block is a *different day*
    min_idx = (
        list(pd.date_range("2024-06-01 09:30", periods=4, freq="min")) +
        list(pd.date_range("2024-06-02 09:30", periods=4, freq="min")) +
        list(pd.date_range("2024-06-03 09:30", periods=4, freq="min"))
    )
    min_df = pd.DataFrame({'Close':[10]*4+[20]*4+[30]*4}, index=pd.DatetimeIndex(min_idx))
    result = daily_sma(daily, min_df, price_type="Close", length=1)
    assert (result[:4]==10).all()
    assert (result[4:8]==20).all()
    assert (result[8:]==30).all()

def test_daily_sma():
    # TODO: add unit test for daily_sma
    assert True  # Placeholder
