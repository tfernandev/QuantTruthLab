import pytest
import pandas as pd
import numpy as np
from core.strategies.factory import StrategyFactory
from core.strategies.base import Strategy

def create_dummy_data():
    # Linear price increase: 100, 101, 102... 120
    prices = np.linspace(100, 120, 20)
    dates = pd.date_range(start='2021-01-01', periods=20, freq='h')
    df = pd.DataFrame({'close': prices}, index=dates)
    return df

def test_sma_crossover_strategy():
    # Setup Data
    # 1. Start low, go high (uptrend) -> SMA Fast > SMA Slow -> Buy
    # 2. Go low (downtrend) -> SMA Fast < SMA Slow -> Sell
    
    # Let's create a sine wave to force crossover
    x = np.linspace(0, 4*np.pi, 100)
    prices = 100 + 10 * np.sin(x)
    dates = pd.date_range(start='2021-01-01', periods=100, freq='h')
    df = pd.DataFrame({'close': prices}, index=dates)
    
    # Params: Fast=5, Slow=15
    params = {'fast_period': 5, 'slow_period': 15}
    strategy = StrategyFactory.get_strategy("SmaCrossover", params)
    
    signals = strategy.generate_signals(df)
    
    assert 'signal' in signals.columns
    assert 'SMA_5' in signals.columns
    assert 'SMA_15' in signals.columns
    
    # Check that we have at least one buy and one sell signal in a wave
    assert (signals['signal'] == 1).any()
    assert (signals['signal'] == -1).any()

def test_rsi_strategy():
    # Create data with extreme movements
    prices = [50] * 20 + [80] * 5 + [20] * 5 # Stable, then Spike (Overbought), then Crash (Oversold)
    dates = pd.date_range(start='2021-01-01', periods=30, freq='h')
    df = pd.DataFrame({'close': prices}, index=dates)
    
    params = {'length': 14, 'overbought': 70, 'oversold': 30}
    strategy = StrategyFactory.get_strategy("RsiStrategy", params)
    
    signals = strategy.generate_signals(df)
    
    # RSI should be high around index 20-25 and low around 25-30
    # Calculations need warm-up, so check end of array
    assert 'RSI_14' in signals.columns

def test_random_strategy_stability():
    # Ensure random strategy produces signals but respects seed (deterministic)
    df = pd.DataFrame({'close': np.random.rand(100)}, index=pd.date_range('2021-01-01', periods=100))
    
    s1 = StrategyFactory.get_strategy("RandomStrategy", {'seed': 42, 'probability': 0.1})
    df1 = s1.generate_signals(df)
    
    s2 = StrategyFactory.get_strategy("RandomStrategy", {'seed': 42, 'probability': 0.1})
    df2 = s2.generate_signals(df)
    
    pd.testing.assert_frame_equal(df1, df2)
    
    # Different seed
    s3 = StrategyFactory.get_strategy("RandomStrategy", {'seed': 999, 'probability': 0.1})
    df3 = s3.generate_signals(df)
    
    # Should be different
    assert not df1['signal'].equals(df3['signal'])
