import pandas as pd
import numpy as np
from .enums import AverageType

class IndicatorUtils:
    @staticmethod
    def ExpAverage(series, length: int):
        return pd.Series(series).ewm(span=length, adjust=False).mean()
    @staticmethod
    def SimpleMovingAvg(series, length: int):
        return pd.Series(series).rolling(window=length, min_periods=1).mean()
    # ... (Other methods as described earlier: Weighted, Wilders, Hull, etc.)
    # See reserved_words.md for full parameter details.
