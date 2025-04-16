import pandas as pd
import numpy as np
import pytest
from tospylib.indicators.stochastic_fast import stochastic_fast

def test_stochastic_fast():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = stochastic_fast(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"K","D"}
    assert len(result) == len(df)
    assert (result['K'] >= 0).all() and (result['K'] <= 100).all()

def test_stochastic_fast_parameters():
    """Test stochastic_fast with different parameters."""
    df = pd.DataFrame({
        'High': range(10, 60),
        'Low': range(1, 51),
        'Close': range(5, 55)
    })
    
    # Test with different K and D periods
    result = stochastic_fast(df['High'], df['Low'], df['Close'], k_period=5, d_period=3)
    assert set(result.columns) == {"K","D"}
    assert len(result) == len(df)
    
    # With shorter periods, we should have fewer NaN values
    assert not result['K'].iloc[5:].isna().any()
    assert not result['D'].iloc[7:].isna().any()  # K period + D period - 1
    
    # Test ranges - both K and D should be within [0, 100]
    assert (result['K'] >= 0).all() and (result['K'] <= 100).all()
    assert (result['D'] >= 0).all() and (result['D'] <= 100).all()

def test_stochastic_fast_error_handling():
    """Test stochastic_fast error handling for various inputs."""
    # Valid inputs for reference
    valid_high = pd.Series(range(10, 30))
    valid_low = pd.Series(range(1, 21))
    valid_close = pd.Series(range(5, 25))
    
    # Test with empty Series
    empty = pd.Series([])
    result_empty = stochastic_fast(empty, empty, empty)
    assert isinstance(result_empty, pd.DataFrame)
    assert len(result_empty) == 0
    
    # Test with Series shorter than required periods
    short = pd.Series(range(1, 5))
    result_short = stochastic_fast(short, short, short)
    assert isinstance(result_short, pd.DataFrame)
    assert len(result_short) == len(short)
    assert result_short['K'].isna().any()  # Some points should be NaN
    
    # Test with non-Series inputs
    list_high = list(range(10, 30))
    list_low = list(range(1, 21))
    list_close = list(range(5, 25))
    result_list = stochastic_fast(list_high, list_low, list_close)
    assert isinstance(result_list, pd.DataFrame)
    assert len(result_list) == len(list_high)
    
    # Test with NaN values
    high_with_nan = pd.Series([10, np.nan, 12, 13, 14, 15, 16, 17, 18, 19] * 2)
    result_nan = stochastic_fast(high_with_nan, valid_low, valid_close)
    assert isinstance(result_nan, pd.DataFrame)
    assert len(result_nan) == len(high_with_nan)
    assert result_nan.isna().any().any()  # Should have some NaN values
    
    # Test with invalid parameter values
    try:
        result_invalid = stochastic_fast(valid_high, valid_low, valid_close, k_period=0)
        # If it doesn't raise, ensure result is valid
        assert isinstance(result_invalid, pd.DataFrame)
    except ValueError:
        pass  # Expected behavior
        
    try:
        result_invalid = stochastic_fast(valid_high, valid_low, valid_close, d_period=-1)
        # If it doesn't raise, ensure result is valid
        assert isinstance(result_invalid, pd.DataFrame)
    except ValueError:
        pass  # Expected behavior

def test_stochastic_fast_edge_cases():
    """Test stochastic_fast with edge cases."""
    # Test with identical High/Low/Close values
    constant = pd.Series([10] * 20)
    result_constant = stochastic_fast(constant, constant, constant)
    assert isinstance(result_constant, pd.DataFrame)
    assert len(result_constant) == len(constant)
    
    # If High = Low = Close, K should be either 100% or NaN
    non_nan_values = result_constant['K'].dropna()
    assert all(val == 100 for val in non_nan_values)
    
    # Test with extreme values (very large price differences)
    high_extreme = pd.Series([1e6] * 20)
    low_extreme = pd.Series([1] * 20)
    close_extreme_high = pd.Series([1e6] * 20)  # Close at highest point
    
    result_extreme_high = stochastic_fast(high_extreme, low_extreme, close_extreme_high)
    assert isinstance(result_extreme_high, pd.DataFrame)
    # K should be 100% when close equals high
    assert all(val == 100 for val in result_extreme_high['K'].dropna())
    
    # Close at lowest point
    close_extreme_low = pd.Series([1] * 20)
    result_extreme_low = stochastic_fast(high_extreme, low_extreme, close_extreme_low)
    # K should be 0% when close equals low
    assert all(val == 0 for val in result_extreme_low['K'].dropna())
    
    # Test with inverted High/Low values
    try:
        # High values below Low values should be handled
        inverted = stochastic_fast(pd.Series([5] * 20), pd.Series([10] * 20), pd.Series([7] * 20))
        assert isinstance(inverted, pd.DataFrame)
    except Exception as e:
        assert "high" in str(e).lower() or "low" in str(e).lower()

def test_stochastic_fast_display_index():
    """Test display_index parameter functionality for stochastic_fast."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=40, freq='D')
    df_daily = pd.DataFrame({
        'High': range(50, 90),
        'Low': range(20, 60),
        'Close': range(35, 75)
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=8, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = stochastic_fast(df_daily['High'], df_daily['Low'], df_daily['Close'])
    result_reindexed = stochastic_fast(
        df_daily['High'], df_daily['Low'], df_daily['Close'], 
        display_index=dates_weekly
    )
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present
    assert set(result_reindexed.columns) == {"K", "D"}
    
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
    result_empty = stochastic_fast(
        df_daily['High'], df_daily['Low'], df_daily['Close'], 
        display_index=empty_index
    )
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"K", "D"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = stochastic_fast(
        df_daily['High'], df_daily['Low'], df_daily['Close'], 
        display_index=different_dates
    )
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"K", "D"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()
