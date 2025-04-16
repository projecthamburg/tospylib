import pandas as pd
import numpy as np
import pytest
from tospylib.indicators.macd import macd

def test_macd():
    """Test basic functionality of MACD."""
    df = pd.DataFrame({'Close': range(1, 41)})  # 40 bars of data
    result = macd(df['Close'])
    
    # Check structure and length
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"Value", "Avg", "Diff"}
    assert len(result) == len(df)
    
    # Check initial NaN values due to EMA calculation
    # Fast EMA (12) should have at least 11 NaN values
    # Slow EMA (26) should have at least 25 NaN values
    assert result['Value'].iloc[:11].isna().all()
    
    # Check for valid values after sufficient data points
    assert not result['Value'].iloc[26:].isna().any()
    assert not result['Avg'].iloc[35:].isna().any()  # Signal (9) needs additional points
    
    # Diff should be Value - Avg
    for i in range(36, 40):  # Check a few points with full calculation
        assert abs(result['Diff'].iloc[i] - (result['Value'].iloc[i] - result['Avg'].iloc[i])) < 1e-10

def test_macd_parameters():
    """Test MACD with custom parameters."""
    df = pd.DataFrame({'Close': range(1, 61)})  # 60 bars of data
    
    # Test with custom parameters
    result = macd(df['Close'], fast_length=8, slow_length=16, signal_length=6)
    
    # Check structure and length
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"Value", "Avg", "Diff"}
    assert len(result) == len(df)
    
    # With these parameters, we should have fewer NaN values
    assert not result['Value'].iloc[16:].isna().any()  # After slow_length
    assert not result['Avg'].iloc[22:].isna().any()    # After slow_length + signal_length
    
    # Diff should be Value - Avg
    for i in range(30, 40):  # Check a few points with full calculation
        assert abs(result['Diff'].iloc[i] - (result['Value'].iloc[i] - result['Avg'].iloc[i])) < 1e-10

def test_macd_error_handling():
    """Test MACD error handling for various inputs."""
    # Test with empty Series
    empty = pd.Series([])
    result_empty = macd(empty)
    assert isinstance(result_empty, pd.DataFrame)
    assert len(result_empty) == 0
    
    # Test with Series shorter than required lengths
    short = pd.Series(range(1, 10))
    result_short = macd(short)
    assert isinstance(result_short, pd.DataFrame)
    assert len(result_short) == len(short)
    assert result_short['Value'].isna().all()  # Not enough data for MACD calculation
    
    # Test with non-Series input
    list_input = list(range(1, 41))
    result_list = macd(list_input)
    assert isinstance(result_list, pd.DataFrame)
    assert len(result_list) == len(list_input)
    
    # Test with NaN values
    with_nan = pd.Series([1, 2, np.nan, 4, 5] * 10)
    result_nan = macd(with_nan)
    assert isinstance(result_nan, pd.DataFrame)
    assert len(result_nan) == len(with_nan)
    assert result_nan.isna().any().any()  # Should have some NaN values
    
    # Test with invalid parameter values
    try:
        result_invalid = macd(pd.Series(range(1, 41)), fast_length=0)
        # If it doesn't raise, ensure result is valid
        assert isinstance(result_invalid, pd.DataFrame)
    except ValueError:
        pass  # Expected behavior
        
    try:
        result_invalid = macd(pd.Series(range(1, 41)), slow_length=-1)
        # If it doesn't raise, ensure result is valid
        assert isinstance(result_invalid, pd.DataFrame)
    except ValueError:
        pass  # Expected behavior

def test_macd_edge_cases():
    """Test MACD with edge cases."""
    # Test with constant values
    constant = pd.Series([10] * 40)
    result_constant = macd(constant)
    assert isinstance(result_constant, pd.DataFrame)
    assert len(result_constant) == len(constant)
    
    # With constant values, MACD Value should approach zero
    assert abs(result_constant['Value'].iloc[-1]) < 1e-5
    
    # Test with extreme values
    extreme = pd.Series([1e9] * 20 + [2e9] * 20)
    result_extreme = macd(extreme)
    assert isinstance(result_extreme, pd.DataFrame)
    assert len(result_extreme) == len(extreme)
    assert not result_extreme.isin([np.inf, -np.inf]).any().any()  # No infinity
    
    # Test with alternating values
    alternating = pd.Series([10, 20] * 20)
    result_alternating = macd(alternating)
    assert isinstance(result_alternating, pd.DataFrame)
    assert len(result_alternating) == len(alternating)

def test_macd_display_index():
    """Test display_index parameter functionality for MACD."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    price_daily = pd.Series(range(1, 51), index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = macd(price_daily)
    result_reindexed = macd(price_daily, display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present
    assert set(result_reindexed.columns) == {"Value", "Avg", "Diff"}
    
    # Verify the values are forward-filled appropriately
    # For dates that exist in both, values should be identical
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        for col in result_normal.columns:
            if pd.isna(result_normal.loc[date, col]) and pd.isna(result_reindexed.loc[date, col]):
                continue  # Both are NaN, which is a match
            else:
                assert result_normal.loc[date, col] == result_reindexed.loc[date, col]
    
    # Test edge case: empty index
    empty_index = pd.DatetimeIndex([])
    result_empty = macd(price_daily, display_index=empty_index)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"Value", "Avg", "Diff"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = macd(price_daily, display_index=different_dates)
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"Value", "Avg", "Diff"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()

def test_macd_length():
    df = pd.DataFrame({'Close': range(1,41)})  # 40 bars of data
    result = macd(df['Close'])
    assert set(result.columns) == {"Value","Avg","Diff"}
    assert len(result) == len(df)

def test_macd_multi_timeframe():
    """Test MACD with data from multiple timeframes."""
    # Create data at different timeframes
    # 1-minute data
    minute_idx = pd.date_range(start='2023-01-01 09:30', periods=300, freq='min')
    minute_data = pd.Series(range(1, 301), index=minute_idx)
    
    # 5-minute data (every 5th point from minute data)
    fivemin_idx = pd.date_range(start='2023-01-01 09:30', periods=60, freq='5min')
    fivemin_data = pd.Series(range(1, 301, 5), index=fivemin_idx)
    
    # Hourly data
    hour_idx = pd.date_range(start='2023-01-01 09:30', periods=50, freq='h')
    hour_data = pd.Series(range(1, 51), index=hour_idx)
    
    # Daily data
    day_idx = pd.date_range(start='2023-01-01', periods=40, freq='D')
    day_data = pd.Series(range(1, 41), index=day_idx)
    
    # Test 1: Calculation should work on all timeframes
    min_result = macd(minute_data, fast_length=5, slow_length=10, signal_length=3)
    fivemin_result = macd(fivemin_data, fast_length=5, slow_length=10, signal_length=3)
    hour_result = macd(hour_data)  # Default parameters
    day_result = macd(day_data)    # Default parameters
    
    # All should produce DataFrames with correct columns
    assert isinstance(min_result, pd.DataFrame)
    assert set(min_result.columns) == {"Value", "Avg", "Diff"}
    assert isinstance(fivemin_result, pd.DataFrame)
    assert set(fivemin_result.columns) == {"Value", "Avg", "Diff"}
    assert isinstance(hour_result, pd.DataFrame)
    assert set(hour_result.columns) == {"Value", "Avg", "Diff"} 
    assert isinstance(day_result, pd.DataFrame)
    assert set(day_result.columns) == {"Value", "Avg", "Diff"}
    
    # Test 2: Calculate on minute data, display at higher timeframes
    result_5min = macd(minute_data, fast_length=5, slow_length=10, signal_length=3, 
                      display_index=fivemin_idx)
    assert len(result_5min) == len(fivemin_idx)
    assert result_5min.index.equals(fivemin_idx)
    
    result_hour = macd(minute_data, fast_length=5, slow_length=10, signal_length=3, 
                      display_index=hour_idx)
    assert len(result_hour) == len(hour_idx)
    assert result_hour.index.equals(hour_idx)
    
    result_day = macd(minute_data, fast_length=5, slow_length=10, signal_length=3, 
                     display_index=day_idx)
    assert len(result_day) == len(day_idx)
    assert result_day.index.equals(day_idx)
    
    # Test 3: Multi-timeframe spanning tests
    # Create a combined index with mixed timeframes
    mixed_idx = pd.DatetimeIndex(list(minute_idx[:10]) + list(hour_idx[5:10]) + list(day_idx[3:7]))
    
    result_mixed = macd(minute_data, fast_length=5, slow_length=10, signal_length=3, 
                       display_index=mixed_idx)
    assert len(result_mixed) == len(mixed_idx)
    assert result_mixed.index.equals(mixed_idx)
    
    # Test 4: Consistency check
    # Values at matching indices should be consistent between original and reindexed
    common_idx = set(minute_idx) & set(fivemin_idx)
    sample_idx = list(common_idx)[10]  # Skip early values which might be NaN
    
    if not pd.isna(min_result.loc[sample_idx, "Value"]) and not pd.isna(result_5min.loc[sample_idx, "Value"]):
        assert abs(min_result.loc[sample_idx, "Value"] - result_5min.loc[sample_idx, "Value"]) < 1e-10

def test_macd_boundary_conditions():
    """Test MACD with boundary conditions and extreme values."""
    # Test with very large length parameters
    data = pd.Series(range(1, 101))
    result = macd(data, fast_length=50, slow_length=80, signal_length=30)
    assert isinstance(result, pd.DataFrame)
    # Most values should be NaN due to large window
    assert result['Value'].iloc[:79].isna().all()  # First slow_length-1 are NaN
    
    # Test with very small length parameters (but valid)
    result_small = macd(data, fast_length=2, slow_length=3, signal_length=2)
    assert isinstance(result_small, pd.DataFrame)
    assert not result_small['Value'].iloc[3:].isna().any()  # Valid after slow_length
    
    # Test with very large values
    large_data = pd.Series([1e9, 2e9, 3e9, 4e9] * 10)
    result_large = macd(large_data)
    assert isinstance(result_large, pd.DataFrame)
    assert not result_large.isin([np.inf, -np.inf]).any().any()  # No infinity
    
    # Test with tiny values
    tiny_data = pd.Series([1e-9, 2e-9, 3e-9, 4e-9] * 10)
    result_tiny = macd(tiny_data)
    assert isinstance(result_tiny, pd.DataFrame)
    assert not result_tiny.isin([np.inf, -np.inf]).any().any()  # No infinity
    
    # Test with mixed extreme values
    extreme_data = pd.Series([1e9, 1e-9, 1e9, 1e-9] * 10)
    result_extreme = macd(extreme_data)
    assert isinstance(result_extreme, pd.DataFrame)
    assert not result_extreme.isin([np.inf, -np.inf]).any().any()  # No infinity
