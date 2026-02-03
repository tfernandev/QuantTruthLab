from fastapi import APIRouter, HTTPException
from typing import List
# No schema import needed here for simple types
# Import from Core (Adjust path if needed based on python path)
import sys
from pathlib import Path

# Add project root to sys path to allow importing 'core'
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from core.data.storage import DataStorage
from core.data.loader import DataLoader

router = APIRouter()

@router.get("/available", response_model=List[str])
def list_available_data():
    """Lists locally available parquet files."""
    storage = DataStorage()
    files = list(storage.base_dir.glob("*.parquet"))
    return [f.name for f in files]

@router.post("/ingest")
def ingest_data(symbol: str, timeframe: str, days: int):
    """Triggers data download."""
    try:
        loader = DataLoader() # This connects to Binance
        storage = DataStorage()
        
        # We need to calc date, simple logic here
        from datetime import datetime, timedelta, timezone
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        df = loader.fetch_ohlcv(symbol, timeframe, since=start_date)
        if df.empty:
             raise HTTPException(status_code=404, detail="No data fetched from exchange")
             
        storage.save_ohlcv(df, symbol, timeframe)
        return {"status": "success", "rows_saved": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
