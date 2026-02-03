from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

class Settings(BaseSettings):
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    DB_DIR: Path = DATA_DIR / "db"
    LOGS_DIR: Path = BASE_DIR / "logs"

    # Exchange Config
    EXCHANGE_ID: str = "binance"
    TIMEFRAMES: list[str] = ["1m", "5m", "15m", "1h", "4h", "1d"]
    
    # Simulation Config
    INITIAL_CAPITAL: float = 10000.0
    MAKER_FEE: float = 0.001
    TAKER_FEE: float = 0.001

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        print(f"Error loading configuration: {e}")
        raise

settings = get_settings()

# Ensure directories exist
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
