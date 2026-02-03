from datetime import datetime, timedelta, timezone
import argparse
from core.data.loader import DataLoader
from core.data.storage import DataStorage
from core.utils.logger import setup_logging, logger

def main(symbol: str, timeframe: str, days: int):
    setup_logging()
    
    loader = DataLoader()
    storage = DataStorage()
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    logger.info(f"Starting ingestion for {symbol} {timeframe} since {start_date}")
    
    df = loader.fetch_ohlcv(symbol, timeframe, since=start_date)
    
    storage.save_ohlcv(df, symbol, timeframe)
    
    logger.success("Ingestion complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest Crypto Data")
    parser.add_argument("--symbol", type=str, default="BTC/USDT", help="Pair symbol")
    parser.add_argument("--tf", type=str, default="1h", help="Timeframe (1m, 5m, 1h, 1d)")
    parser.add_argument("--days", type=int, default=30, help="Days of history to fetch")
    
    args = parser.parse_args()
    main(args.symbol, args.tf, args.days)
