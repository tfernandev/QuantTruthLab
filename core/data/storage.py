import pandas as pd
from pathlib import Path
from core.config import settings
from core.utils.logger import logger

class DataStorage:
    def __init__(self, base_dir: Path = settings.PROCESSED_DATA_DIR):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, symbol: str, timeframe: str) -> Path:
        # Normalize symbol: BTC/USDT -> BTC_USDT
        safe_symbol = symbol.replace("/", "_")
        return self.base_dir / f"{safe_symbol}_{timeframe}.parquet"

    def save_ohlcv(self, df: pd.DataFrame, symbol: str, timeframe: str):
        """Saves OHLCV data to parquet."""
        if df.empty:
            logger.warning(f"No data to save for {symbol} {timeframe}")
            return

        file_path = self._get_file_path(symbol, timeframe)
        
        # Ensure timestamp is index
        if 'timestamp' in df.columns:
            df.set_index('timestamp', inplace=True)
        
        # Sort by index
        df.sort_index(inplace=True)

        try:
            # If file exists, merge (simplified for now: overwrite or append could be complex with parquet chunks)
            # For robustness in this MVP, we will simpler overwrite or read-concat-write
            if file_path.exists():
                existing_df = pd.read_parquet(file_path)
                combined = pd.concat([existing_df, df])
                combined = combined[~combined.index.duplicated(keep='last')] # Deduplicate
                combined.sort_index(inplace=True)
                combined.to_parquet(file_path, compression='snappy')
                logger.info(f"Updated data for {symbol} {timeframe}. Rows: {len(combined)}")
            else:
                df.to_parquet(file_path, compression='snappy')
                logger.info(f"Saved new data for {symbol} {timeframe}. Rows: {len(df)}")
                
        except Exception as e:
            logger.error(f"Failed to save data for {symbol} {timeframe}: {e}")
            raise

    def load_ohlcv(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """Loads OHLCV data. If timeframe is not 1h, it resamples from 1h."""
        if timeframe == "1h":
             return self._load_from_parquet(symbol, "1h")
        
        # Load 1h and resample
        df_1h = self._load_from_parquet(symbol, "1h")
        if df_1h.empty:
            return df_1h
            
        return self._resample(df_1h, timeframe)

    def _load_from_parquet(self, symbol: str, timeframe: str) -> pd.DataFrame:
        file_path = self._get_file_path(symbol, timeframe)
        if not file_path.exists():
            return pd.DataFrame()
        try:
            df = pd.read_parquet(file_path)
            cols = ['open', 'high', 'low', 'close', 'volume']
            df[cols] = df[cols].astype(float)
            return df
        except Exception as e:
            logger.error(f"Failed to load: {e}")
            return pd.DataFrame()

    def _resample(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Resamples 1h data to higher timeframes."""
        # Map CCXT/Standard timeframes to Pandas aliases
        mapping = {"4h": "4h", "1d": "1D", "12h": "12h"}
        alias = mapping.get(timeframe)
        if not alias:
            logger.warning(f"Unsupported resampling timeframe: {timeframe}")
            return df

        resampler = df.resample(alias)
        resampled_df = resampler.agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        
        return resampled_df
