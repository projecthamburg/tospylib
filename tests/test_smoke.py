import pandas as pd
from tospylib.indicators.simple_moving_avg import simple_moving_avg
from tospylib.indicators.mov_avg_exponential import mov_avg_exponential
from tospylib.indicators.daily_sma import daily_sma
from tospylib.indicators.relative_strength import relative_strength
from tospylib.indicators.macd import macd
from tospylib.indicators.bollinger_bands import bollinger_bands
from tospylib.indicators.stochastic_fast import stochastic_fast
from tospylib.indicators.adx import adx
from tospylib.indicators.ichimoku import ichimoku
from tospylib.indicators.obv import obv
from tospylib.indicators.volume_weighted_macd import volume_weighted_macd
from tospylib.indicators.pivot_points import pivot_points

def test_smoke():
    # Create a sample time series with OHLCV data
    idx = pd.date_range("2024-06-01", periods=100)
    df = pd.DataFrame({
        'Open': range(100, 200),
        'High': range(110, 210),
        'Low': range(90, 190),
        'Close': range(100, 200),
        'Volume': [1000] * 100
    }, index=idx)
    
    # Test each indicator
    # Simple Moving Average
    sma = simple_moving_avg(df['Close'], length=20)
    assert not sma.isnull().all()
    
    # Exponential Moving Average
    ema = mov_avg_exponential(df['Close'], length=20)
    assert not ema.isnull().all()
    
    # Daily SMA
    daily = daily_sma(df, df, price_type="Close", length=1)
    assert not daily.isnull().all()
    
    # Relative Strength
    rsi = relative_strength(df['Close'], length=14)
    assert not rsi.isnull().all()
    
    # MACD
    macd_out = macd(df['Close'])
    assert not macd_out.isnull().all().all()
    
    # Bollinger Bands
    bb = bollinger_bands(df['Close'], length=20)
    assert not bb.isnull().all().all()
    
    # Stochastic Fast
    stoch = stochastic_fast(df['High'], df['Low'], df['Close'])
    assert not stoch.isnull().all().all()
    
    # ADX
    adx_out = adx(df['High'], df['Low'], df['Close'])
    assert not adx_out.isnull().all().all()
    
    # Ichimoku
    ichi = ichimoku(df['High'], df['Low'], df['Close'])
    assert not ichi.isnull().all().all()
    
    # OBV
    obv_out = obv(df['Close'], df['Volume'])
    assert not obv_out.isnull().all()
    
    # Volume Weighted MACD
    vw_macd = volume_weighted_macd(df['Close'], df['Volume'])
    assert not vw_macd.isnull().all().all()
    
    # Pivot Points
    pp = pivot_points(df['High'], df['Low'], df['Close'])
    assert not pp.isnull().all().all() 