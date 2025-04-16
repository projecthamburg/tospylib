import pandas as pd
import numpy as np
import pytest
from tospylib.indicators.obv import obv

def test_obv():
    df = pd.DataFrame({
        'Close': [10, 11, 10, 12, 11],
        'Volume': [100, 200, 150, 300, 250]
    })
    result = obv(df['Close'], df['Volume'])
    assert len(result) == len(df)
    assert result.iloc[-1] != 0  # Should have some value

def test_obv_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = obv(df['Close'], df['Volume'])
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)

def test_obv_error_handling_input_types():
    """Test how OBV handles invalid input types."""
    # Valid inputs for comparison
    valid_close = pd.Series([10, 11, 10, 12, 11])
    valid_volume = pd.Series([100, 200, 150, 300, 250])
    
    # Test with non-Series inputs for close
    non_series_inputs = [
        [10, 11, 10, 12, 11],  # List
        np.array([10, 11, 10, 12, 11]),  # NumPy array
        10,  # Scalar
        "10, 11, 10, 12, 11",  # String
        {"a": 10, "b": 11}  # Dictionary
    ]
    
    for invalid_input in non_series_inputs:
        # OBV should convert these to Series with proper handling
        result = obv(invalid_input, valid_volume)
        # The result should be a Series
        assert isinstance(result, pd.Series)
        
        # If it's scalar or list/array-like with same length, results should match or be NaN
        if isinstance(invalid_input, (list, np.ndarray)) and len(invalid_input) == len(valid_volume):
            assert len(result) >= len(valid_volume)
    
    # Test with non-Series inputs for volume
    for invalid_input in non_series_inputs:
        result = obv(valid_close, invalid_input)
        assert isinstance(result, pd.Series)
        
        # If it's scalar or list/array-like with same length, results should match or be NaN
        if isinstance(invalid_input, (list, np.ndarray)) and len(invalid_input) == len(valid_close):
            assert len(result) >= len(valid_close)
            
    # Test specific error handling in lines 40-43
    # Test with totally invalid inputs that should trigger error handling
    try:
        # Pass complex objects that can't be converted to numeric Series
        result = obv(complex(1, 2), complex(2, 3))
        # If it doesn't raise an error, check the output is still a Series
        assert isinstance(result, pd.Series)
        assert result.isna().all()  # Should be all NaN
    except Exception as e:
        # If it raises, make sure the error is handled gracefully
        assert "invalid" in str(e).lower() or "convert" in str(e).lower()
    
    # Test with unparseable string inputs
    try:
        result = obv("not a number", "also not a number")
        # If it returns a result, it should be all NaN
        assert isinstance(result, pd.Series)
        assert result.isna().all()
    except Exception as e:
        # If it raises, error message should be clear
        assert "convert" in str(e).lower() or "invalid" in str(e).lower()
        
    # Test with None values
    try:
        result = obv(None, valid_volume)
        # If it returns, check it's handled properly
        assert isinstance(result, pd.Series)
    except Exception as e:
        # If it raises, make sure the error is clear
        assert "none" in str(e).lower() or "invalid" in str(e).lower()

def test_obv_different_length_series():
    """Test how OBV handles Series of different lengths."""
    close = pd.Series([10, 11, 10, 12, 11])
    volume_shorter = pd.Series([100, 200, 150])
    volume_longer = pd.Series([100, 200, 150, 300, 250, 200, 100])
    
    # Test with shorter volume series
    result = obv(close, volume_shorter)
    # The result should have a length that is the outer join of the two indices
    assert len(result) >= 3  # At least as long as the shortest series
    assert len(result) <= 5  # At most as long as the longest series
        
    # Test with longer volume series
    result = obv(close, volume_longer)
    # When the series are different lengths, the updated implementation joins them
    # and the result should be the length of the union of indices
    assert len(result) >= 5  # At least as long as shortest series
    assert len(result) <= 7  # At most as long as longest series

def test_obv_nan_values():
    """Test how OBV handles NaN values in input series."""
    # Series with NaN in close
    close_with_nan = pd.Series([10, np.nan, 10, 12, 11])
    normal_volume = pd.Series([100, 200, 150, 300, 250])
    
    result = obv(close_with_nan, normal_volume)
    # Expect result to have same length
    assert len(result) == len(close_with_nan)
    # NaN in close should result in NaN in output
    assert result.isna().sum() >= close_with_nan.isna().sum()
    # Verify NaN at same position
    assert result.isna().iloc[1] == True
    
    # Series with NaN in volume
    normal_close = pd.Series([10, 11, 10, 12, 11])
    volume_with_nan = pd.Series([100, np.nan, 150, 300, 250])
    
    result = obv(normal_close, volume_with_nan)
    # Expect result to have same length
    assert len(result) == len(normal_close)
    # NaN in volume should result in NaN in output at that position and possibly after
    assert result.isna().sum() >= 1
    # Verify NaN at position with NaN volume
    assert result.isna().iloc[1] == True

def test_obv_edge_cases():
    """Test how OBV handles edge cases like empty series or single values."""
    # Empty Series
    empty_close = pd.Series([])
    empty_volume = pd.Series([])
    
    result = obv(empty_close, empty_volume)
    # Empty input should result in empty output
    assert len(result) == 0
    
    # Single-value Series
    single_close = pd.Series([10])
    single_volume = pd.Series([100])
    
    result = obv(single_close, single_volume)
    # Since OBV needs at least 2 values to compute differences,
    # a single-element series should return a single value
    assert len(result) == 1
    assert result.iloc[0] == 0  # Initial OBV value should be 0
    
    # Extreme values
    large_close = pd.Series([1e10, 1e10 + 1, 1e10, 1e10 + 2])
    large_volume = pd.Series([1e10, 1e10, 1e10, 1e10])
    
    result = obv(large_close, large_volume)
    # It should handle large values correctly
    assert len(result) == len(large_close)
    assert not result.isin([np.inf, -np.inf]).any()  # No infinity values
    
    # Negative values in volume
    close_normal = pd.Series([10, 11, 10, 12])
    volume_negative = pd.Series([100, -200, 150, 300])
    
    result = obv(close_normal, volume_negative)
    # It should handle negative values
    assert len(result) == len(close_normal)

def test_obv_display_index():
    """Test display_index parameter functionality for OBV."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    df_daily = pd.DataFrame({
        'Close': range(1, 51),
        'Volume': [100] * 50
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = obv(df_daily['Close'], df_daily['Volume'])
    result_reindexed = obv(df_daily['Close'], df_daily['Volume'], display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify the values are forward-filled appropriately
    # For dates that exist in both, values should be identical
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        assert result_normal.loc[date] == result_reindexed.loc[date]
    
    # Test edge case: empty index
    # Should return empty series
    empty_index = pd.DatetimeIndex([])
    result_empty = obv(df_daily['Close'], df_daily['Volume'], display_index=empty_index)
    assert len(result_empty) == 0
    
    # Test with DatetimeIndex that has completely different dates
    # Should still work with forward-filling
    different_dates = pd.date_range(start='2023-02-01', periods=5, freq='D')
    result_diff_dates = obv(df_daily['Close'], df_daily['Volume'], display_index=different_dates)
    assert len(result_diff_dates) == len(different_dates)
    
    # Test with mixed index types - integer index display_index
    int_index = pd.Index([100, 200, 300, 400, 500])
    result_int_index = obv(df_daily['Close'], df_daily['Volume'], display_index=int_index)
    assert len(result_int_index) == len(int_index)
