import ccxt
import pandas as pd
from datetime import datetime, timezone
import time
from core.utils.logger import logger
from core.config import settings

class DataLoader:
    def __init__(self, exchange_id: str = "binance"):
        self.exchange_class = getattr(ccxt, exchange_id)
        self.exchange = self.exchange_class({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot' # Default to spot
            }
        })
        logger.info(f"Initialized DataLoader for {exchange_id}")

    def fetch_ohlcv(self, symbol: str, timeframe: str, since: datetime = None, limit: int = 1000) -> pd.DataFrame:
        """
        Fetches OHLCV data from exchange.
        Handles pagination automatically if needed (basic version fetches one batch or loops if implemented).
        For backtesting, we usually need a lot of history.
        """
        if since is None:
            # Default to a reasonable start time if not provided, e.g., 30 days ago
            # But usually we provide a specific start date.
            logger.warning("No 'since' date provided, fetching latest 1000 candles.")
            since_ts = None
        else:
            since_ts = int(since.timestamp() * 1000)

        all_ohlcv = []
        
        try:
            logger.info(f"Fetching {symbol} {timeframe} from {since}")
            while True:
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since=since_ts, limit=limit)
                if not ohlcv:
                    break
                
                all_ohlcv.extend(ohlcv)
                
                # Update since_ts for next batch
                last_ts = ohlcv[-1][0]
                since_ts = last_ts + 1
                
                # Basic progress log
                logger.debug(f"Fetched {len(ohlcv)} candles. Last: {pd.to_datetime(last_ts, unit='ms')}")

                # If we got fewer than limit, we reached the end
                if len(ohlcv) < limit:
                    break
                
                # Safety break for huge requests (can be refined)
                if len(all_ohlcv) > 100_000:
                    logger.warning("Reached safety limit of 100k candles.")
                    break

            df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"Total fetched: {len(df)} rows for {symbol} {timeframe}")
            return df

        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    def get_supported_timeframes(self):
        return self.exchange.timeframes
