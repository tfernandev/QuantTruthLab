from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, List
from core.utils.logger import logger

class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    Strategies should implement `generate_signals`.
    """
    def __init__(self, name: str, params: Dict[str, Any] = None):
        self.name = name
        self.params = params or {}
        logger.info(f"Strategy initialized: {self.name} with params: {self.params}")

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes OHLCV data and returns a DataFrame with a 'signal' column.
        """
        pass

    @abstractmethod
    def describe(self) -> str:
        """Human-readable description of the strategy."""
        pass

    @abstractmethod
    def parameters_schema(self) -> List[Dict[str, Any]]:
        """Schema for UI to render parameter controls."""
        pass
    
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            logger.warning("Strategy received empty DataFrame")
            return df
            
        logger.debug(f"Running strategy {self.name} on {len(df)} rows")
        result = self.generate_signals(df)
        return result
