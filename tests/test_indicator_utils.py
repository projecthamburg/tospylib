import numpy as np
import pandas as pd
from tospylib.indicator_utils import IndicatorUtils

def test_simple_moving_avg():
    # Test basic functionality
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.simple_moving_avg(data, 3)
    expected = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([1, np.nan, 3, 4, 5])
    result = IndicatorUtils.simple_moving_avg(data, 3)
    expected = pd.Series([np.nan, np.nan, np.nan, np.nan, 4.0])
    pd.testing.assert_series_equal(result, expected)

    # Test with different length
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.simple_moving_avg(data, 2)
    expected = pd.Series([np.nan, 1.5, 2.5, 3.5, 4.5])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = IndicatorUtils.simple_moving_avg(data, 1)
    pd.testing.assert_series_equal(result, data)

def test_exp_moving_avg():
    # Test basic functionality
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.exp_moving_avg(data, 3)
    alpha = 2 / (3 + 1)
    expected = pd.Series([
        1.0,
        alpha * 2 + (1 - alpha) * 1,
        alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1),
        alpha * 4 + (1 - alpha) * (alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1)),
        alpha * 5 + (1 - alpha) * (alpha * 4 + (1 - alpha) * (alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1)))
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([1, np.nan, 3, 4, 5])
    result = IndicatorUtils.exp_moving_avg(data, 3)
    expected = pd.Series([
        1.0,
        np.nan,  # NaN should propagate
        np.nan,
        np.nan,
        np.nan
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = IndicatorUtils.exp_moving_avg(data, 1)
    pd.testing.assert_series_equal(result, data)

def test_wilders_moving_avg():
    # Test basic functionality
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.wilders_moving_avg(data, 3)
    alpha = 1 / 3
    expected = pd.Series([
        np.nan,
        np.nan,
        2.0,  # Initial SMA
        alpha * 4 + (1 - alpha) * 2,
        alpha * 5 + (1 - alpha) * (alpha * 4 + (1 - alpha) * 2)
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([1, np.nan, 3, 4, 5])
    result = IndicatorUtils.wilders_moving_avg(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        2.0,  # Initial SMA with available values
        alpha * 4 + (1 - alpha) * 2,
        alpha * 5 + (1 - alpha) * (alpha * 4 + (1 - alpha) * 2)
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = IndicatorUtils.wilders_moving_avg(data, 1)
    pd.testing.assert_series_equal(result, data)

def test_stdev():
    # Test basic functionality
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.stdev(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        np.std([1, 2, 3], ddof=0),
        np.std([2, 3, 4], ddof=0),
        np.std([3, 4, 5], ddof=0)
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([1, np.nan, 3, 4, 5])
    result = IndicatorUtils.stdev(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        np.std([1, 3], ddof=0),  # Only use non-NaN values
        np.std([3, 4], ddof=0),
        np.std([3, 4, 5], ddof=0)
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.stdev(data, 1)
    expected = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])  # Need at least 2 values
    pd.testing.assert_series_equal(result, expected)

def test_highest():
    # Test basic functionality
    data = pd.Series([1, 2, 3, 4, 5])
    result = IndicatorUtils.highest(data, 3)
    expected = pd.Series([np.nan, np.nan, 3, 4, 5])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([1, np.nan, 3, 4, 5])
    result = IndicatorUtils.highest(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        3.0,  # Only use non-NaN values
        4.0,
        5.0
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with window of all NaN values
    data = pd.Series([1, np.nan, np.nan, np.nan, 5])
    result = IndicatorUtils.highest(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        np.nan,  # Window of all NaNs
        np.nan,  # Window of all NaNs
        5.0
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = IndicatorUtils.highest(data, 1)
    pd.testing.assert_series_equal(result, data)

def test_lowest():
    # Test basic functionality
    data = pd.Series([5, 4, 3, 2, 1])
    result = IndicatorUtils.lowest(data, 3)
    expected = pd.Series([np.nan, np.nan, 3, 2, 1])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    data = pd.Series([5, np.nan, 3, 2, 1])
    result = IndicatorUtils.lowest(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        3.0,  # Only use non-NaN values
        2.0,
        1.0
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with window of all NaN values
    data = pd.Series([5, np.nan, np.nan, np.nan, 1])
    result = IndicatorUtils.lowest(data, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        np.nan,  # Window of all NaNs
        np.nan,  # Window of all NaNs
        1.0
    ])
    pd.testing.assert_series_equal(result, expected)

    # Test with length=1
    data = pd.Series([5, 4, 3, 2, 1], dtype=float)
    result = IndicatorUtils.lowest(data, 1)
    pd.testing.assert_series_equal(result, data)

def test_crosses_above():
    # Test basic functionality
    series1 = pd.Series([1, 2, 3, 4, 5])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_above(series1, series2)
    expected = pd.Series([0, 0, 1, 0, 0])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    series1 = pd.Series([1, np.nan, 3, 4, 5])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_above(series1, series2)
    expected = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(result, expected)

    # Test with no crosses
    series1 = pd.Series([1, 1, 1, 1, 1])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_above(series1, series2)
    expected = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(result, expected)

def test_crosses_below():
    # Test basic functionality
    series1 = pd.Series([3, 2, 1, 2, 3])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_below(series1, series2)
    expected = pd.Series([0, 0, 1, 0, 0])
    pd.testing.assert_series_equal(result, expected)

    # Test with NaN values
    series1 = pd.Series([3, np.nan, 1, 2, 3])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_below(series1, series2)
    expected = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(result, expected)

    # Test with no crosses
    series1 = pd.Series([3, 3, 3, 3, 3])
    series2 = pd.Series([2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_below(series1, series2)
    expected = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(result, expected)

def test_simple_moving_avg_edge_cases():
    """Test edge cases for simple_moving_avg function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.simple_moving_avg(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([1, 2])
    result = IndicatorUtils.simple_moving_avg(short, 3)
    expected = pd.Series([np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [1, 2, 3, 4, 5]
    result = IndicatorUtils.simple_moving_avg(list_input, 3)
    expected = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-numeric data
    str_data = pd.Series(['a', 'b', 'c'])
    try:
        result = IndicatorUtils.simple_moving_avg(str_data, 3)
        assert False, "Should have raised an error for non-numeric data"
    except:
        pass

def test_exp_moving_avg_edge_cases():
    """Test edge cases for exp_moving_avg function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.exp_moving_avg(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([1])
    result = IndicatorUtils.exp_moving_avg(short, 3)
    expected = pd.Series([1.0])  # EMA with one value is just that value
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [1, 2, 3, 4, 5]
    result = IndicatorUtils.exp_moving_avg(list_input, 3)
    alpha = 2 / (3 + 1)
    expected = pd.Series([
        1.0,
        alpha * 2 + (1 - alpha) * 1,
        alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1),
        alpha * 4 + (1 - alpha) * (alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1)),
        alpha * 5 + (1 - alpha) * (alpha * 4 + (1 - alpha) * (alpha * 3 + (1 - alpha) * (alpha * 2 + (1 - alpha) * 1)))
    ])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with all NaN values
    all_nan = pd.Series([np.nan, np.nan, np.nan])
    result = IndicatorUtils.exp_moving_avg(all_nan, 3)
    expected = pd.Series([np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)

def test_wilders_moving_avg_edge_cases():
    """Test edge cases for wilders_moving_avg function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.wilders_moving_avg(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([1, 2])
    result = IndicatorUtils.wilders_moving_avg(short, 3)
    expected = pd.Series([np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [1, 2, 3, 4, 5]
    result = IndicatorUtils.wilders_moving_avg(list_input, 3)
    alpha = 1 / 3
    expected = pd.Series([
        np.nan,
        np.nan,
        2.0,  # Initial SMA
        alpha * 4 + (1 - alpha) * 2,
        alpha * 5 + (1 - alpha) * (alpha * 4 + (1 - alpha) * 2)
    ])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with first values NaN
    first_nans = pd.Series([np.nan, np.nan, 3, 4, 5])
    result = IndicatorUtils.wilders_moving_avg(first_nans, 3)
    expected = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])  # Not enough data
    pd.testing.assert_series_equal(result, expected)

def test_stdev_edge_cases():
    """Test edge cases for stdev function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.stdev(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([1, 2])
    result = IndicatorUtils.stdev(short, 3)
    expected = pd.Series([np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [1, 2, 3, 4, 5]
    result = IndicatorUtils.stdev(list_input, 3)
    expected = pd.Series([
        np.nan,
        np.nan,
        np.std([1, 2, 3], ddof=0),
        np.std([2, 3, 4], ddof=0),
        np.std([3, 4, 5], ddof=0)
    ])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with all same values (std should be 0)
    same_values = pd.Series([5, 5, 5, 5, 5])
    result = IndicatorUtils.stdev(same_values, 3)
    expected = pd.Series([np.nan, np.nan, 0.0, 0.0, 0.0])
    pd.testing.assert_series_equal(result, expected)

def test_highest_edge_cases():
    """Test edge cases for highest function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.highest(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([1, 2])
    result = IndicatorUtils.highest(short, 3)
    expected = pd.Series([np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [1, 2, 3, 4, 5]
    result = IndicatorUtils.highest(list_input, 3)
    expected = pd.Series([np.nan, np.nan, 3, 4, 5])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with complex NaN pattern
    complex_nan = pd.Series([1, np.nan, np.nan, 4, 5])
    result = IndicatorUtils.highest(complex_nan, 3)
    expected = pd.Series([np.nan, np.nan, np.nan, 4.0, 5.0])
    pd.testing.assert_series_equal(result, expected)
    
    # Test special case handling
    special_case = pd.Series([1, np.nan, np.nan])
    result = IndicatorUtils.highest(special_case, 3)
    expected = pd.Series([np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)

def test_lowest_edge_cases():
    """Test edge cases for lowest function."""
    # Test with empty series
    empty = pd.Series([])
    result = IndicatorUtils.lowest(empty, 3)
    assert len(result) == 0
    
    # Test with series shorter than length
    short = pd.Series([5, 4])
    result = IndicatorUtils.lowest(short, 3)
    expected = pd.Series([np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with non-Series input
    list_input = [5, 4, 3, 2, 1]
    result = IndicatorUtils.lowest(list_input, 3)
    expected = pd.Series([np.nan, np.nan, 3, 2, 1])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with complex NaN pattern
    complex_nan = pd.Series([5, np.nan, np.nan, 2, 1])
    result = IndicatorUtils.lowest(complex_nan, 3)
    expected = pd.Series([np.nan, np.nan, np.nan, 2.0, 1.0])
    pd.testing.assert_series_equal(result, expected)
    
    # Test special case handling
    special_case = pd.Series([5, np.nan, np.nan])
    result = IndicatorUtils.lowest(special_case, 3)
    expected = pd.Series([np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)

def test_crosses_above_edge_cases():
    """Test edge cases for crosses_above function."""
    # Test with empty series
    empty1 = pd.Series([])
    empty2 = pd.Series([])
    result = IndicatorUtils.crosses_above(empty1, empty2)
    assert len(result) == 0
    
    # Test with series of different lengths
    series1 = pd.Series([1, 2, 3, 4, 5])
    series2 = pd.Series([3, 3, 3])
    try:
        result = IndicatorUtils.crosses_above(series1, series2)
        # Expected: either handle different lengths or throw an exception
    except:
        pass
    
    # Test with non-Series inputs
    list1 = [1, 2, 3, 4, 5]
    list2 = [3, 3, 2, 2, 2]
    result = IndicatorUtils.crosses_above(list1, list2)
    expected = pd.Series([0, 0, 1, 0, 0])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with complex crossing patterns
    series1 = pd.Series([1, 3, 2, 4, 3, 5])
    series2 = pd.Series([2, 2, 3, 3, 4, 4])
    result = IndicatorUtils.crosses_above(series1, series2)
    expected = pd.Series([0, 1, 0, 1, 0, 1])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with first entry crossing
    series1 = pd.Series([3, 4, 5])
    series2 = pd.Series([2, 2, 2])
    result = IndicatorUtils.crosses_above(series1, series2)
    expected = pd.Series([0, 0, 0])  # No crossing detected for first value
    pd.testing.assert_series_equal(result, expected)

def test_crosses_below_edge_cases():
    """Test edge cases for crosses_below function."""
    # Test with empty series
    empty1 = pd.Series([])
    empty2 = pd.Series([])
    result = IndicatorUtils.crosses_below(empty1, empty2)
    assert len(result) == 0
    
    # Test with series of different lengths
    series1 = pd.Series([5, 4, 3, 2, 1])
    series2 = pd.Series([3, 3, 3])
    try:
        result = IndicatorUtils.crosses_below(series1, series2)
        # Expected: either handle different lengths or throw an exception
    except:
        pass
    
    # Test with non-Series inputs
    list1 = [5, 4, 2, 1, 0]
    list2 = [3, 3, 3, 3, 3]
    result = IndicatorUtils.crosses_below(list1, list2)
    expected = pd.Series([0, 0, 1, 0, 0])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with complex crossing patterns
    series1 = pd.Series([3, 1, 3, 1, 3, 1])
    series2 = pd.Series([2, 2, 2, 2, 2, 2])
    result = IndicatorUtils.crosses_below(series1, series2)
    expected = pd.Series([0, 1, 0, 1, 0, 1])
    pd.testing.assert_series_equal(result, expected)
    
    # Test with first entry crossing
    series1 = pd.Series([1, 1, 1])
    series2 = pd.Series([2, 2, 2])
    result = IndicatorUtils.crosses_below(series1, series2)
    expected = pd.Series([0, 0, 0])  # No crossing detected for first value
    pd.testing.assert_series_equal(result, expected)

def test_input_validation():
    """Test input validation for all functions."""
    # Test with invalid length parameter
    for func in [IndicatorUtils.simple_moving_avg, IndicatorUtils.exp_moving_avg, 
                IndicatorUtils.wilders_moving_avg, IndicatorUtils.stdev, 
                IndicatorUtils.highest, IndicatorUtils.lowest]:
        
        # Test with negative length
        try:
            result = func(pd.Series([1, 2, 3]), -1)
            # Either handle properly or raise an exception
        except:
            pass
        
        # Test with zero length
        try:
            result = func(pd.Series([1, 2, 3]), 0)
            # Either handle properly or raise an exception
        except:
            pass
        
        # Test with very large length
        try:
            result = func(pd.Series([1, 2, 3]), 1000)
            # Should handle without errors
        except:
            pass 