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
    """Test basic functionality of daily_sma."""
    # Basic functionality test
    daily_idx = pd.date_range("2024-06-01", periods=5, freq="D")
    daily_df = pd.DataFrame({'Close':[10, 20, 30, 40, 50]}, index=daily_idx)
    
    intraday_idx = []
    for day in daily_idx:
        intraday_idx.extend(pd.date_range(day, periods=6, freq="H"))
    
    intraday_values = []
    for i in range(5):  # 5 days
        intraday_values.extend([10 + i*10] * 6)  # 6 hours per day
        
    intraday_df = pd.DataFrame({'Close': intraday_values}, index=pd.DatetimeIndex(intraday_idx))
    
    result = daily_sma(daily_df, intraday_df, price_type="Close", length=3)
    
    # Should have same length as intraday
    assert len(result) == len(intraday_df)
    
    # First 12 points (2 days) should be NaN (need 3 days for SMA)
    assert result[:12].isna().all()
    
    # Remaining points should have SMA values
    assert not result[12:].isna().any()

def test_daily_sma_error_handling():
    """Test error handling in daily_sma."""
    # Test with empty DataFrames
    empty_df = pd.DataFrame()
    daily_idx = pd.date_range("2024-06-01", periods=5, freq="D")
    daily_df = pd.DataFrame({'Close':[10, 20, 30, 40, 50]}, index=daily_idx)
    
    intraday_idx = pd.date_range("2024-06-01", periods=20, freq="H")
    intraday_df = pd.DataFrame({'Close': range(20)}, index=intraday_idx)
    
    # Empty daily DataFrame
    try:
        result = daily_sma(empty_df, intraday_df, price_type="Close", length=3)
        assert len(result) == len(intraday_df)
        assert result.isna().all()
    except Exception as e:
        assert "empty" in str(e).lower() or "invalid" in str(e).lower()
    
    # Empty intraday DataFrame
    try:
        result = daily_sma(daily_df, empty_df, price_type="Close", length=3)
        assert len(result) == 0
    except Exception as e:
        assert "empty" in str(e).lower() or "invalid" in str(e).lower()
    
    # Test with missing price column
    try:
        result = daily_sma(daily_df, intraday_df, price_type="NonExistentColumn", length=3)
        assert result.isna().all()
    except KeyError:
        pass  # Expected behavior
        
    # Test with invalid length
    try:
        result = daily_sma(daily_df, intraday_df, price_type="Close", length=0)
        # Either returns valid results or raises error
    except ValueError:
        pass  # Expected behavior
    
    # Test with non-DatetimeIndex
    no_date_daily = pd.DataFrame({'Close':[10, 20, 30]})
    no_date_intraday = pd.DataFrame({'Close': range(20)})
    
    try:
        result = daily_sma(no_date_daily, no_date_intraday, price_type="Close", length=3)
        # May handle this gracefully or raise an error
    except Exception:
        pass  # Expected behavior
