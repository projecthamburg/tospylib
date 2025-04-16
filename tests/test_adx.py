import pandas as pd
from tospylib.indicators.adx import adx

def test_adx():
    df = pd.DataFrame({
        'High': range(10, 50),
        'Low': range(1, 41),
        'Close': range(5, 45)
    })
    result = adx(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"ADX", "+DI", "-DI"}
    assert len(result) == len(df)
    assert (result['ADX'] >= 0).all() and (result['ADX'] <= 100).all()

def test_adx_smoke():
    df = pd.read_csv('ohlcv_sample.csv')
    result = adx(df['High'], df['Low'], df['Close'])
    assert set(result.columns) == {"ADX", "+DI", "-DI"}
    assert len(result) == len(df)

def test_adx_display_index():
    """Test display_index parameter functionality."""
    # Create test data with daily dates
    dates_daily = pd.date_range(start='2023-01-01', periods=50, freq='D')
    df_daily = pd.DataFrame({
        'High': range(10, 60),
        'Low': range(1, 51),
        'Close': range(5, 55)
    }, index=dates_daily)
    
    # Create a weekly date index (fewer points)
    dates_weekly = pd.date_range(start='2023-01-01', periods=10, freq='W')
    
    # Test reindexing from daily to weekly
    result_normal = adx(df_daily['High'], df_daily['Low'], df_daily['Close'])
    result_reindexed = adx(df_daily['High'], df_daily['Low'], df_daily['Close'], 
                          display_index=dates_weekly)
    
    # Verify the reindexed result has the correct index
    assert len(result_reindexed) == len(dates_weekly)
    assert (result_reindexed.index == dates_weekly).all()
    
    # Verify all columns are present in reindexed result
    assert set(result_reindexed.columns) == {"ADX", "+DI", "-DI"}
    
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
    # Should return empty dataframe with same columns
    empty_index = pd.DatetimeIndex([])
    result_empty = adx(df_daily['High'], df_daily['Low'], df_daily['Close'],
                      display_index=empty_index)
    assert len(result_empty) == 0
    assert set(result_empty.columns) == {"ADX", "+DI", "-DI"}
    
    # Test with dates outside the original range
    different_dates = pd.date_range(start='2023-03-01', periods=5, freq='D')
    result_diff = adx(df_daily['High'], df_daily['Low'], df_daily['Close'],
                     display_index=different_dates)
    assert isinstance(result_diff, pd.DataFrame)
    assert len(result_diff) == len(different_dates)
    assert set(result_diff.columns) == {"ADX", "+DI", "-DI"}
    # Should have values (forward-filled)
    assert not result_diff.isna().all().all()
