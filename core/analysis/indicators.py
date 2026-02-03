import pandas as pd
import pandas_ta as ta

class TechnicalAnalysis:
    """
    Wrapper around pandas_ta to provide consistent indicator API.
    """
    
    @staticmethod
    def add_sma(df: pd.DataFrame, length: int = 20, column: str = "close") -> pd.DataFrame:
        """Adds Simple Moving Average."""
        df[f"SMA_{length}"] = df[column].rolling(window=length).mean()
        return df

    @staticmethod
    def add_rsi(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """Adds RSI."""
        df.ta.cores = 0
        df.ta.rsi(length=length, append=True)
        return df
    
    @staticmethod
    def add_ema(df: pd.DataFrame, length: int = 20) -> pd.DataFrame:
        """Adds EMA."""
        df.ta.cores = 0
        df.ta.ema(length=length, append=True)
        return df

    @staticmethod
    def add_atr(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """Adds Average True Range (useful for volatility-based stops)."""
        df.ta.cores = 0
        df.ta.atr(length=length, append=True)
        return df

    @staticmethod
    def add_bbands(df: pd.DataFrame, length: int = 20, std: float = 2.0) -> pd.DataFrame:
        """Adds Bollinger Bands."""
        df.ta.cores = 0
        df.ta.bbands(length=length, std=std, append=True)
        return df

    @staticmethod
    def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Adds MACD."""
        df.ta.cores = 0
        df.ta.macd(fast=fast, slow=slow, signal=signal, append=True)
        return df
