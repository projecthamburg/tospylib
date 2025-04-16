import pandas as pd
from tospylib.indicators.ichimoku import ichimoku

def test_ichimoku():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = ichimoku(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"Tenkan","Kijun","SenkouA","SenkouB","Chikou"}
    assert len(result) == len(df)

def test_ichimoku_display_index():
    """Test display_index parameter functionality for Ichimoku."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=100, freq='D')
    df_daily = pd.DataFrame({
        'High': range(10, 110),
        'Low': range(1, 101),
        'Close': range(5, 105)
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=20, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = ichimoku(df_daily['High'], df_daily['Low'], df_daily['Close'])
    result_reindexed = ichimoku(df_daily['High'], df_daily['Low'], df_daily['Close'], 
                              display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present in reindexed result
    assert set(result_reindexed.columns) == {"Tenkan", "Kijun", "SenkouA", "SenkouB", "Chikou"}
    
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
    result_empty = ichimoku(df_daily['High'], df_daily['Low'], df_daily['Close'],
                          display_index=empty_index)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"Tenkan", "Kijun", "SenkouA", "SenkouB", "Chikou"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-05-01', periods=5, freq='D')
    result_diff = ichimoku(df_daily['High'], df_daily['Low'], df_daily['Close'],
                         display_index=different_dates)
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"Tenkan", "Kijun", "SenkouA", "SenkouB", "Chikou"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()
