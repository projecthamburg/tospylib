import pandas as pd
import numpy as np
import pytest
from tospylib.indicators.relative_strength import relative_strength

def test_relative_strength():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = relative_strength(df['Close'], length=3)
    assert len(result) == len(df)
    assert result.iloc[-1] > 0  # Should be positive

def test_relative_strength_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = relative_strength(df['Close'], length=14)
    assert isinstance(result, pd.Series)
    assert len(result) == len(df)

def test_relative_strength_error_handling_input_types():
    """Test how Relative Strength handles invalid input types."""
    # Valid inputs for comparison
    valid_price = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
    
    # Test with non-Series inputs
    non_series_inputs = [
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],  # List
        np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19]),  # NumPy array
        10,  # Scalar
        "10, 11, 12",  # String
        {"a": 10, "b": 20}  # Dictionary
    ]
    
    for invalid_input in non_series_inputs:
        # Should handle different input types
        try:
            result = relative_strength(invalid_input, length=3)
            # If it doesn't raise, it should return valid RSI values
            assert isinstance(result, pd.Series)
            # RSI values should be between 0 and 100
            assert ((result >= 0) & (result <= 100)).all() or result.isna().any()
        except Exception as e:
            # If it raises, make sure it's a relevant error for non-numeric inputs
            assert isinstance(e, (TypeError, ValueError, AttributeError))

def test_relative_strength_line46_error_handling():
    """Test specific error handling on line 46 of relative_strength.py."""
    # Line 46 likely handles division calculation in RSI formula
    # Create test data that might trigger division by zero or other calculation errors
    
    # Case 1: All identical values (would give zero in division)
    all_identical = pd.Series([10, 10, 10, 10, 10, 10])
    result = relative_strength(all_identical, length=3)
    # This should return a specific value (50 for RSI) or NaN, but not fail
    assert isinstance(result, pd.Series)
    assert result.iloc[-1] == 50 or np.isnan(result.iloc[-1])
    
    # Case 2: All upward moves (would give infinity or very large values)
    all_up = pd.Series([10, 11, 12, 13, 14, 15])
    result = relative_strength(all_up, length=3)
    # This should return a valid RSI near 100, but not fail
    assert isinstance(result, pd.Series)
    assert result.iloc[-1] > 90 or np.isnan(result.iloc[-1])
    
    # Case 3: All downward moves (would give near-zero values)
    all_down = pd.Series([15, 14, 13, 12, 11, 10])
    result = relative_strength(all_down, length=3)
    # This should return a valid RSI near 0, but not fail
    assert isinstance(result, pd.Series)
    assert result.iloc[-1] < 10 or np.isnan(result.iloc[-1])
    
    # Case 4: Alternating values (would test averaging logic)
    alternating = pd.Series([10, 15, 10, 15, 10, 15])
    result = relative_strength(alternating, length=3)
    # Should return a valid RSI, typically around 50 for alternating
    assert isinstance(result, pd.Series)
    assert 40 <= result.iloc[-1] <= 60 or np.isnan(result.iloc[-1])
    
    # Case 5: Extreme values (might cause overflow)
    extreme = pd.Series([1e8, 2e8, 1e8, 2e8, 1e8, 2e8])
    result = relative_strength(extreme, length=3)
    # Should handle large values without overflow
    assert isinstance(result, pd.Series)
    assert not pd.isna(result.iloc[-1]) and 0 <= result.iloc[-1] <= 100

def test_relative_strength_parameters():
    """Test how Relative Strength handles different parameter values."""
    price = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
    
    # Test various lengths
    for length in [1, 2, 5, 14, 50]:
        result = relative_strength(price, length=length)
        assert isinstance(result, pd.Series)
        assert len(result) == len(price)
        # RSI values should be between 0 and 100
        # Some NaN values might be present for the first few periods
        valid_values = result.dropna()
        assert ((valid_values >= 0) & (valid_values <= 100)).all()
    
    # Test displace parameter
    for displace in [-5, -1, 0, 1, 5]:
        result = relative_strength(price, length=3, displace=displace)
        assert isinstance(result, pd.Series)
        assert len(result) == len(price)

def test_relative_strength_nan_values():
    """Test how Relative Strength handles NaN values."""
    # Create a series with NaN values
    price_with_nan = pd.Series([10, np.nan, 12, 13, np.nan, 15, 16, 17, 18, 19])
    
    # Calculate RSI with NaN values
    result = relative_strength(price_with_nan, length=3)
    assert isinstance(result, pd.Series)
    assert len(result) == len(price_with_nan)
    
    # NaN values in input should result in some NaN values in output
    assert result.isna().any()
    
    # All NaN inputs should result in all NaN outputs
    all_nan = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])
    result_all_nan = relative_strength(all_nan, length=3)
    assert result_all_nan.isna().all()

def test_relative_strength_edge_cases():
    """Test edge cases for Relative Strength calculation."""
    # Empty series
    empty = pd.Series([])
    result_empty = relative_strength(empty, length=3)
    assert isinstance(result_empty, pd.Series)
    assert len(result_empty) == 0
    
    # Single value series (not enough for RSI)
    single = pd.Series([10])
    result_single = relative_strength(single, length=3)
    assert isinstance(result_single, pd.Series)
    assert len(result_single) == 1
    assert result_single.isna().all()  # Not enough data points for RSI
    
    # Series with all same values (no change)
    constant = pd.Series([10, 10, 10, 10, 10])
    result_constant = relative_strength(constant, length=3)
    assert isinstance(result_constant, pd.Series)
    assert len(result_constant) == len(constant)
    # With no change, RSI is undefined (div by zero) or 50
    assert pd.isna(result_constant.iloc[-1]) or result_constant.iloc[-1] == 50
    
    # Series with all increasing values
    increasing = pd.Series([10, 11, 12, 13, 14, 15])
    result_increasing = relative_strength(increasing, length=3)
    # For all increasing values, RSI should approach 100
    assert result_increasing.iloc[-1] > 60
    
    # Series with all decreasing values
    decreasing = pd.Series([15, 14, 13, 12, 11, 10])
    result_decreasing = relative_strength(decreasing, length=3)
    # For all decreasing values, RSI should approach 0
    assert result_decreasing.iloc[-1] < 40
    
    # Extreme values
    large = pd.Series([1e10, 2e10, 3e10, 4e10, 5e10])
    result_large = relative_strength(large, length=3)
    assert isinstance(result_large, pd.Series)
    assert len(result_large) == len(large)
    # Should handle large values correctly
    assert not result_large.isin([np.inf, -np.inf]).any()
    
    # Zero and negative values
    zero_neg = pd.Series([0, -1, -2, -3, -2, -1, 0])
    result_zero_neg = relative_strength(zero_neg, length=3)
    assert isinstance(result_zero_neg, pd.Series)
    assert len(result_zero_neg) == len(zero_neg)
    
    # Price with no change followed by changes
    mixed = pd.Series([10, 10, 10, 12, 11, 13])
    result_mixed = relative_strength(mixed, length=3)
    assert isinstance(result_mixed, pd.Series)
    assert len(result_mixed) == len(mixed)

def test_relative_strength_display_index():
    """Test display_index parameter functionality for Relative Strength."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    price_daily = pd.Series(range(1, 51), index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = relative_strength(price_daily, length=14)
    result_reindexed = relative_strength(price_daily, length=14, display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify the values are forward-filled appropriately
    # For dates that exist in both, values should be identical
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        assert result_normal.loc[date] == result_reindexed.loc[date]
    
    # Test edge case: empty index
    empty_index = pd.DatetimeIndex([])
    result_empty = relative_strength(price_daily, length=14, display_index=empty_index)
    assert isinstance(result_empty, pd.Series)
    assert len(result_empty) == 0
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = relative_strength(price_daily, length=14, display_index=different_dates)
    assert isinstance(result_diff, pd.Series)
    assert len(result_diff) == len(different_dates)
    # Should have values (forward-filled)
    assert not result_diff.isna().all()

    # Test index preservation
    assert all(result_reindexed.index == dates_weekly)
    
    # Test content is identical for common dates
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        if pd.isna(result_normal.loc[date]) and pd.isna(result_reindexed.loc[date]):
            continue  # Both are NaN, which is a match
        else:
            assert result_normal.loc[date] == result_reindexed.loc[date]
