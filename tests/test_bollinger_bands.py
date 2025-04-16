import pandas as pd
from tospylib.indicators.bollinger_bands import bollinger_bands

def test_bollinger_bands_smoke():
    s = pd.Series(range(1,22))
    result = bollinger_bands(s, length=5)
    assert set(result.columns) == {"MidLine", "LowerBand", "UpperBand"}
    assert len(result) == len(s)

def test_bollinger_bands_display_index():
    """Test display_index parameter functionality for Bollinger Bands."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    price_daily = pd.Series(range(1, 51), index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = bollinger_bands(price_daily, length=20)
    result_reindexed = bollinger_bands(price_daily, length=20, display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present in reindexed result
    assert set(result_reindexed.columns) == {"MidLine", "LowerBand", "UpperBand"}
    
    # Verify that values are correctly forward-filled
    # Since the implementation might now fill NaNs with 0, we focus on checking
    # that non-zero values are preserved correctly
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        for col in result_normal.columns:
            if pd.isna(result_normal.loc[date, col]) and pd.isna(result_reindexed.loc[date, col]):
                continue  # Both are NaN, which is a match
            else:
                assert result_normal.loc[date, col] == result_reindexed.loc[date, col]
    
    # Test edge case: empty index
    # Should return empty dataframe with same columns
    empty_index = pd.DatetimeIndex([])
    result_empty = bollinger_bands(price_daily, display_index=empty_index)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"MidLine", "LowerBand", "UpperBand"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = bollinger_bands(price_daily, length=20, display_index=different_dates)
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"MidLine", "LowerBand", "UpperBand"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()
