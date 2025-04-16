import numpy as np
import pandas as pd
from .enums import AverageType

class IndicatorUtils:
    @staticmethod
    def simple_moving_avg(series, length):
        series = pd.Series(series)
        sma = np.full(len(series), np.nan)
        for i in range(length-1, len(series)):
            window = series.iloc[i-length+1:i+1]
            if window.isnull().any():
                continue
            sma[i] = window.mean()
        return pd.Series(sma, index=series.index)

    @staticmethod
    def exp_moving_avg(series, length):
        alpha = 2 / (length + 1)
        series = pd.Series(series)
        ema = np.full(len(series), np.nan)
        for i in range(len(series)):
            if np.isnan(series.iloc[i]):
                continue
            if i == 0:
                ema[i] = series.iloc[i]
            else:
                ema[i] = alpha * series.iloc[i] + (1 - alpha) * ema[i-1]
        return pd.Series(ema, index=series.index)

    @staticmethod
    def wilders_moving_avg(series, length):
        alpha = 1 / length
        series = pd.Series(series)
        wma = np.full(len(series), np.nan)
        for i in range(len(series)):
            if np.isnan(series.iloc[i]):
                continue
            if i < length-1:
                continue  # Not enough data for initial SMA
            elif i == length-1:
                wma[i] = series.iloc[:length].mean()
            else:
                wma[i] = alpha * series.iloc[i] + (1 - alpha) * wma[i-1]
        return pd.Series(wma, index=series.index)

    @staticmethod
    def stdev(series, length):
        series = pd.Series(series)
        stdevs = np.full(len(series), np.nan)
        for i in range(length-1, len(series)):
            window = series.iloc[i-length+1:i+1]
            stdevs[i] = window.std(ddof=0)
        return pd.Series(stdevs, index=series.index)

    @staticmethod
    def highest(series, length):
        series = pd.Series(series)
        out = np.full(len(series), np.nan)
        for i in range(length-1, len(series)):
            out[i] = series.iloc[i-length+1:i+1].max()
        return pd.Series(out, index=series.index)

    @staticmethod
    def lowest(series, length):
        series = pd.Series(series)
        out = np.full(len(series), np.nan)
        for i in range(length-1, len(series)):
            out[i] = series.iloc[i-length+1:i+1].min()
        return pd.Series(out, index=series.index)

    @staticmethod
    def crosses_above(series1, series2):
        s1, s2 = pd.Series(series1), pd.Series(series2)
        crosses = (s1 > s2) & (s1.shift(1) <= s2.shift(1))
        # Return bool mask or integer 1/0 as you prefer for signals
        return crosses.astype(int)

    @staticmethod
    def crosses_below(series1, series2):
        s1, s2 = pd.Series(series1), pd.Series(series2)
        crosses = (s1 < s2) & (s1.shift(1) >= s2.shift(1))
        return crosses.astype(int)
