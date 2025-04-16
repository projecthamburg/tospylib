import pandas as pd
from tospylib.indicators.mov_avg_exponential import mov_avg_exponential

def test_mov_avg_exponential():
    df = pd.DataFrame({'Close':[1,2,3,4,5,6,7,8,9,10]})
    result = mov_avg_exponential(df['Close'], length=3)
    assert len(result) == len(df)
    assert result.iloc[-1] > 0  # Should be positive

def test_mov_avg_exponential_display_index():
    """Test display_index parameter functionality for EMA."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    price_daily = pd.Series(range(1, 51), index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = mov_avg_exponential(price_daily, length=9)
    result_reindexed = mov_avg_exponential(price_daily, length=9, display_index=dates_weekly)
    
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
    result_empty = mov_avg_exponential(price_daily, display_index=empty_index)
    assert len(result_empty) == 0
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = mov_avg_exponential(price_daily, length=9, display_index=different_dates)
    assert isinstance(result_diff, pd.Series)
    assert len(result_diff) == len(different_dates)
    # Should have values (forward-filled)
    assert not result_diff.isna().all()

    # Test index preservation
    assert all(result_reindexed.index == dates_weekly)
