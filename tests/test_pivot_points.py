import pandas as pd
import numpy as np
import pytest
from tospylib.indicators.pivot_points import pivot_points

def test_pivot_points():
    df = pd.DataFrame({
        'High': [10, 20, 30],
        'Low': [5, 15, 25],
        'Close': [8, 18, 28]
    })
    result = pivot_points(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    assert len(result) == len(df)

def test_pivot_points_error_handling_input_types():
    """Test how Pivot Points handles invalid input types."""
    # Valid inputs for comparison
    valid_high = pd.Series([10, 20, 30])
    valid_low = pd.Series([5, 15, 25])
    valid_close = pd.Series([8, 18, 28])
    
    # Test with non-Series inputs
    non_series_inputs = [
        [10, 20, 30],  # List
        np.array([10, 20, 30]),  # NumPy array
        10,  # Scalar
        "10, 20, 30",  # String
        {"a": 10, "b": 20}  # Dictionary
    ]
    
    # Test non-Series high input
    for invalid_input in non_series_inputs:
        # Should convert these to Series or raise a clear error
        result = pivot_points(invalid_input, valid_low, valid_close)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
        # If input is list/array with same length, result should have same length
        if isinstance(invalid_input, (list, np.ndarray)) and len(invalid_input) == len(valid_low):
            assert len(result) == len(valid_low)
    
    # Test non-Series low input
    for invalid_input in non_series_inputs:
        result = pivot_points(valid_high, invalid_input, valid_close)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Test non-Series close input
    for invalid_input in non_series_inputs:
        result = pivot_points(valid_high, valid_low, invalid_input)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}

def test_pivot_points_timeframe():
    """Test handling of different timeframe values."""
    df = pd.DataFrame({
        'High': [10, 20, 30],
        'Low': [5, 15, 25],
        'Close': [8, 18, 28]
    })
    
    # Valid timeframes
    valid_timeframes = ["DAY", "WEEK", "MONTH"]
    for tf in valid_timeframes:
        result = pivot_points(df['High'], df['Low'], df['Close'], timeframe=tf)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
        assert len(result) == len(df)
    
    # Invalid timeframe should raise ValueError
    with pytest.raises(ValueError):
        pivot_points(df['High'], df['Low'], df['Close'], timeframe="INVALID")
    
    # Case-sensitivity check
    with pytest.raises(ValueError):
        pivot_points(df['High'], df['Low'], df['Close'], timeframe="day")
        
    # Test line 47 specifically: timeframe validation
    # Test with integer timeframe
    try:
        result = pivot_points(df['High'], df['Low'], df['Close'], timeframe=1)
        # If it doesn't raise, make sure the result is valid
        assert isinstance(result, pd.DataFrame)
    except ValueError as e:
        # If it raises, error should be clear
        assert "timeframe" in str(e).lower()
        
    # Test with invalid but string-like timeframe
    try:
        result = pivot_points(df['High'], df['Low'], df['Close'], timeframe="QUARTER")
        # If it doesn't raise, make sure the result is valid
        assert isinstance(result, pd.DataFrame)
    except ValueError as e:
        # If it raises, error should be clear about valid options
        assert "day" in str(e).lower() or "week" in str(e).lower() or "month" in str(e).lower()

def test_pivot_points_different_length_series():
    """Test how Pivot Points handles series of different lengths."""
    high = pd.Series([10, 20, 30])
    low = pd.Series([5, 15])  # Shorter
    close = pd.Series([8, 18, 28, 38])  # Longer
    
    # Test with series of different lengths
    # The result should have a length based on index alignment
    result = pivot_points(high, low, close)
    # Should have combined all unique indices with outer join
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Test with index-aligned series of different lengths
    high_idx = pd.Series([10, 20, 30], index=[0, 1, 2])
    low_idx = pd.Series([5, 15], index=[0, 1])
    close_idx = pd.Series([8, 18, 28, 38], index=[0, 1, 2, 3])
    
    result_idx = pivot_points(high_idx, low_idx, close_idx)
    assert isinstance(result_idx, pd.DataFrame)
    assert set(result_idx.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    # Should contain all indices from all series
    assert len(result_idx) >= max(len(high_idx), len(low_idx), len(close_idx))

def test_pivot_points_nan_values():
    """Test how Pivot Points handles NaN values."""
    # Create test data with NaN values
    high = pd.Series([10, np.nan, 30])
    low = pd.Series([5, 15, np.nan])
    close = pd.Series([8, 18, 28])
    
    # Calculate with NaN values
    result = pivot_points(high, low, close)
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # NaN in input should result in NaN in output for that row
    assert result.iloc[1].isna().any() or result.iloc[2].isna().any()
    
    # All NaN inputs should result in all NaN outputs
    all_nan = pd.Series([np.nan, np.nan, np.nan])
    result_all_nan = pivot_points(all_nan, all_nan, all_nan)
    assert result_all_nan.isna().all().all()

def test_pivot_points_edge_cases():
    """Test edge cases like empty series, single values, etc."""
    # Empty series
    empty = pd.Series([])
    result_empty = pivot_points(empty, empty, empty)
    assert isinstance(result_empty, pd.DataFrame)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Single value
    single = pd.Series([10])
    single_low = pd.Series([5])
    single_close = pd.Series([8])
    result_single = pivot_points(single, single_low, single_close)
    assert isinstance(result_single, pd.DataFrame)
    assert len(result_single) == 1
    assert set(result_single.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Extreme values
    large = pd.Series([1e10, 2e10])
    large_low = pd.Series([9e9, 1.9e10])
    large_close = pd.Series([9.5e9, 1.95e10])
    result_large = pivot_points(large, large_low, large_close)
    assert isinstance(result_large, pd.DataFrame)
    assert len(result_large) == 2
    assert not result_large.isin([np.inf, -np.inf]).any().any()  # No infinity
    
    # Zero and negative values
    zero_neg = pd.Series([0, -10])
    zero_neg_low = pd.Series([-5, -15])
    zero_neg_close = pd.Series([-2, -12])
    result_zero_neg = pivot_points(zero_neg, zero_neg_low, zero_neg_close)
    assert isinstance(result_zero_neg, pd.DataFrame)
    assert len(result_zero_neg) == 2
    # Pivot points can be negative with negative inputs
    assert (result_zero_neg < 0).any().any()

def test_pivot_points_display_index():
    """Test display_index parameter functionality for Pivot Points."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=30, freq='D')
    df_daily = pd.DataFrame({
        'High': range(100, 130),
        'Low': range(50, 80),
        'Close': range(75, 105)
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=6, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = pivot_points(df_daily['High'], df_daily['Low'], df_daily['Close'])
    result_reindexed = pivot_points(
        df_daily['High'], df_daily['Low'], df_daily['Close'],
        display_index=dates_weekly
    )
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present
    assert set(result_reindexed.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Verify the values are forward-filled appropriately
    # For dates that exist in both, values should be identical
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        pd.testing.assert_series_equal(
            result_normal.loc[date],
            result_reindexed.loc[date]
        )
    
    # Test edge case: empty index
    empty_index = pd.DatetimeIndex([])
    result_empty = pivot_points(
        df_daily['High'], df_daily['Low'], df_daily['Close'],
        display_index=empty_index
    )
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"PP","R1","R2","R3","S1","S2","S3"}
    
    # Test with a completely different date range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = pivot_points(
        df_daily['High'], df_daily['Low'], df_daily['Close'],
        display_index=different_dates
    )
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"PP","R1","R2","R3","S1","S2","S3"}

def test_pivot_points_line64_error_handling():
    """Test error handling specifically for line 64."""
    # Line 64 likely handles calculation of pivot points
    # Test with extreme values that might cause calculation issues
    high = pd.Series([np.inf, 20, 30])
    low = pd.Series([5, -np.inf, 25])
    close = pd.Series([8, 18, 28])
    
    # Calculate with infinity values
    try:
        result = pivot_points(high, low, close)
        # If it doesn't raise, check for proper handling
        assert isinstance(result, pd.DataFrame)
        # The rows with infinity should have NaN values
        assert result.iloc[0].isna().any() or result.iloc[1].isna().any()
    except Exception as e:
        # If it raises, make sure error is handled gracefully
        assert "infinity" in str(e).lower() or "invalid" in str(e).lower()
    
    # Test with all zeros (could cause division by zero)
    zeros_high = pd.Series([0, 0, 0])
    zeros_low = pd.Series([0, 0, 0])
    zeros_close = pd.Series([0, 0, 0])
    
    try:
        result = pivot_points(zeros_high, zeros_low, zeros_close)
        # If successful, check if output makes sense
        assert isinstance(result, pd.DataFrame)
        # With all zero inputs, outputs should be zero or NaN
        assert (result == 0).all().all() or result.isna().any().any()
    except Exception as e:
        # If it raises, check error message
        assert "zero" in str(e).lower() or "invalid" in str(e).lower()