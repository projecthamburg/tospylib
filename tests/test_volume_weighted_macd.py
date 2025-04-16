import pandas as pd
from tospylib.indicators.volume_weighted_macd import volume_weighted_macd

def test_volume_weighted_macd():
    df = pd.DataFrame({
        'Close': range(1,41),
        'Volume': [100] * 40
    })
    result = volume_weighted_macd(df['Close'], df['Volume'])
    assert set(result.columns) == {"Value","Avg","Diff"}
    assert len(result) == len(df)

def test_volume_weighted_macd_display_index():
    """Test display_index parameter functionality for Volume Weighted MACD."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    df_daily = pd.DataFrame({
        'Close': range(1, 51),
        'Volume': [100] * 50
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = volume_weighted_macd(df_daily['Close'], df_daily['Volume'])
    result_reindexed = volume_weighted_macd(df_daily['Close'], df_daily['Volume'], 
                                          display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present in reindexed result
    assert set(result_reindexed.columns) == {"Value", "Avg", "Diff"}
    
    # Verify that values are correctly forward-filled
    common_dates = set(result_normal.index) & set(dates_weekly)
    for date in common_dates:
        for col in result_normal.columns:
            if pd.isna(result_normal.loc[date, col]) and pd.isna(result_reindexed.loc[date, col]):
                continue  # Both are NaN, which is a match
            else:
                assert result_reindexed.loc[date, col] == result_normal.loc[date, col]
    
    # Test edge case: empty index
    empty_index = pd.DatetimeIndex([])
    result_empty = volume_weighted_macd(df_daily['Close'], df_daily['Volume'],
                                      display_index=empty_index)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"Value", "Avg", "Diff"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = volume_weighted_macd(df_daily['Close'], df_daily['Volume'],
                                     display_index=different_dates)
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"Value", "Avg", "Diff"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()
