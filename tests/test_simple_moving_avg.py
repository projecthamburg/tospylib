import pandas as pd
from tospylib.indicators.simple_moving_avg import simple_moving_avg
import numpy as np

def test_simple_moving_avg():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = simple_moving_avg(df['Close'], length=3)
    assert round(result.iloc[-1],5) == 9.0  # Last three: 8,9,10

def test_simple_moving_avg_display_index():
    """Test display_index parameter functionality for Simple Moving Average."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    price_daily = pd.Series(range(1, 51), index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = simple_moving_avg(price_daily, length=9)
    result_reindexed = simple_moving_avg(price_daily, length=9, display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify the values are forward-filled appropriately
    # For dates that exist in both, values should be identical
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        if pd.isna(result_normal.loc[date]) and pd.isna(result_reindexed.loc[date]):
            continue  # Both are NaN, which is a match
        else:
            assert result_normal.loc[date] == result_reindexed.loc[date]
    
    # Test edge case: empty index
    # Should return empty series
    empty_index = pd.DatetimeIndex([])
    result_empty = simple_moving_avg(price_daily, display_index=empty_index)
    assert len(result_empty) == 0
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = simple_moving_avg(price_daily, length=9, display_index=different_dates)
    assert isinstance(result_diff, pd.Series)
    assert len(result_diff) == len(different_dates)
    # Should have values (forward-filled)
    assert not result_diff.isna().all()

    # Test index preservation
    assert all(result_reindexed.index == dates_weekly)

def test_simple_moving_avg_multi_timeframe():
    """Test simple_moving_avg across different timeframes."""
    # Create data at different timeframes
    # 1-minute data
    minute_idx = pd.date_range(start='2023-01-01 09:30', periods=300, freq='min')
    minute_data = pd.Series(range(1, 301), index=minute_idx)
    
    # 5-minute data (every 5th point from minute data)
    fivemin_idx = pd.date_range(start='2023-01-01 09:30', periods=60, freq='5min')
    fivemin_data = pd.Series(range(1, 301, 5), index=fivemin_idx)
    
    # Hourly data
    hour_idx = pd.date_range(start='2023-01-01 09:30', periods=24, freq='h')
    hour_data = pd.Series(range(1, 25), index=hour_idx)
    
    # Daily data
    day_idx = pd.date_range(start='2023-01-01', periods=10, freq='D')
    day_data = pd.Series(range(1, 11), index=day_idx)
    
    # Test 1: Calculation should work identically on all timeframes
    length = 3
    min_result = simple_moving_avg(minute_data, length=length)
    fivemin_result = simple_moving_avg(fivemin_data, length=length)
    hour_result = simple_moving_avg(hour_data, length=length)
    day_result = simple_moving_avg(day_data, length=length)
    
    # All should have NaN for first (length-1) values
    assert min_result.iloc[:length-1].isna().all()
    assert fivemin_result.iloc[:length-1].isna().all()
    assert hour_result.iloc[:length-1].isna().all()
    assert day_result.iloc[:length-1].isna().all()
    
    # Values after length should be valid
    assert not min_result.iloc[length:].isna().any()
    assert not fivemin_result.iloc[length:].isna().any()
    assert not hour_result.iloc[length:].isna().any()
    assert not day_result.iloc[length:].isna().any()
    
    # Test 2: Calculation across timeframes with display_index
    # Calculate SMA on minute data, display at 5-minute intervals
    result_reindexed = simple_moving_avg(minute_data, length=length, display_index=fivemin_idx)
    assert len(result_reindexed) == len(fivemin_idx)
    
    # Test 3: Calculate on low timeframe, verify against higher timeframe
    # For common timestamps, the calculation on 5-min should match the reindexed 1-min
    common_times = set(fivemin_idx) & set(result_reindexed.index)
    for time in common_times:
        if pd.isna(fivemin_result.loc[time]) and pd.isna(result_reindexed.loc[time]):
            continue  # Both are NaN, which is a match
        elif not pd.isna(fivemin_result.loc[time]) and not pd.isna(result_reindexed.loc[time]):
            # Check values are close enough (may have small float differences)
            assert abs(fivemin_result.loc[time] - result_reindexed.loc[time]) < 1e-10
    
    # Test 4: Multi-timeframe spanning tests
    # Create a combined index with mixed timeframes
    mixed_idx = pd.DatetimeIndex(list(minute_idx[:10]) + list(hour_idx[5:10]) + list(day_idx[3:7]))
    
    result_mixed = simple_moving_avg(minute_data, length=length, display_index=mixed_idx)
    assert len(result_mixed) == len(mixed_idx)
    assert result_mixed.index.equals(mixed_idx)

def test_simple_moving_avg_boundary_conditions():
    """Test simple_moving_avg with boundary conditions and extreme values."""
    # Test with very large length (larger than data)
    data = pd.Series(range(1, 11))
    result = simple_moving_avg(data, length=20)
    assert result.isna().all()  # All values should be NaN
    
    # Test with very large values
    large_data = pd.Series([1e9, 2e9, 3e9, 4e9, 5e9])
    result = simple_moving_avg(large_data, length=3)
    assert not result.isna().all()  # Should handle large values
    assert not result.isin([np.inf, -np.inf]).any()  # No infinity
    
    # Test with very small values
    small_data = pd.Series([1e-9, 2e-9, 3e-9, 4e-9, 5e-9])
    result = simple_moving_avg(small_data, length=3)
    assert not result.isna().all()  # Should handle small values
    
    # Test with alternating extreme values
    extreme_data = pd.Series([1e9, 1e-9, 1e9, 1e-9, 1e9])
    result = simple_moving_avg(extreme_data, length=3)
    assert not result.isin([np.inf, -np.inf]).any()  # No infinity
    
    # Test with length exactly equal to data length
    exact_data = pd.Series(range(1, 6))
    result = simple_moving_avg(exact_data, length=5)
    assert len(result) == len(exact_data)
    assert result.iloc[:-1].isna().all()  # All but last should be NaN
    assert not pd.isna(result.iloc[-1])  # Last value should be valid
