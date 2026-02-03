import pandas as pd
import pandas_ta as ta
from core.strategies.base import Strategy
from core.analysis.indicators import TechnicalAnalysis as TA

class SmaCrossoverStrategy(Strategy):
    """
    Classic SMA Crossover Strategy.
    Buy when fast SMA crosses above slow SMA.
    Sell when fast SMA crosses below slow SMA.
    """
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        fast_period = int(self.params.get('fast_period', 10))
        slow_period = int(self.params.get('slow_period', 20))
        
        # Calculate Indicators
        # We work on a copy to avoid side effects if reused
        df = df.copy()
        
        # Uses pandas_ta extension or our wrapper
        # Let's use our wrapper for consistency in 'src' but pandas_ta is powerful directly
        TA.add_sma(df, length=fast_period)
        TA.add_sma(df, length=slow_period)
        
        col_fast = f"SMA_{fast_period}"
        col_slow = f"SMA_{slow_period}"
        
        # Logic
        df['signal'] = 0
        
        # Bullish Crossover
        crossover_bull = (df[col_fast] > df[col_slow]) & (df[col_fast].shift(1) <= df[col_slow].shift(1))
        
        # Bearish Crossover
        crossover_bear = (df[col_fast] < df[col_slow]) & (df[col_fast].shift(1) >= df[col_slow].shift(1))
        
        df.loc[crossover_bull, 'signal'] = 1
        df.loc[crossover_bear, 'signal'] = -1
        
        return df

    def describe(self) -> str:
        return "Estrategia clásica de seguimiento de tendencia basada en el cruce de dos medias móviles simples."

    def parameters_schema(self) -> list:
        return [
            {"name": "fast_period", "label": "Periodo Rápido", "type": "number", "default": 10},
            {"name": "slow_period", "label": "Periodo Lento", "type": "number", "default": 20}
        ]
