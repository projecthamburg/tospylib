# tospylib
A Python library of Thinkscript-equivalent technical indicators, designed for research, backtesting, and systematic trading using pandas dataframes.

## Indicators Included
- SimpleMovingAvg
- MovAvgExponential
- DailySMA
- RelativeStrength
- MACD
- BollingerBands
- StochasticFast
- ADX
- Ichimoku
- OnBalanceVolume (OBV)
- VolumeWeightedMACD
- PivotPoints

## Usage Example
```python
import pandas as pd
from tospylib import simple_moving_avg

df = pd.read_csv('ohlcv.csv', parse_dates=['Date'], index_col='Date')
sma = simple_moving_avg(df['Close'], length=9, displace=0, display_index=df.index)
df['SMA'] = sma
```
See docs, code, and `reserved_words.md` for Thinkscript parameter translation.
