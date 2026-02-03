import sys
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from core.data.loader import DataLoader
from core.data.storage import DataStorage
from core.utils.logger import setup_logging, logger

def build_datasets():
    setup_logging()
    loader = DataLoader()
    storage = DataStorage()
    
    symbols = ["BTC/USDT", "ETH/USDT"]
    timeframe = "1h"
    
    # We want data from 2021 to now. 
    # Approx 4 years = 1460 days.
    start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
    
    for symbol in symbols:
        logger.info(f"Building dataset for {symbol}...")
        try:
            df = loader.fetch_ohlcv(symbol, timeframe, since=start_date)
            if not df.empty:
                storage.save_ohlcv(df, symbol, timeframe)
                logger.success(f"Dataset ready for {symbol}: {len(df)} rows.")
            else:
                logger.error(f"Failed to fetch data for {symbol}")
        except Exception as e:
            logger.error(f"Error building dataset for {symbol}: {e}")

if __name__ == "__main__":
    build_datasets()
