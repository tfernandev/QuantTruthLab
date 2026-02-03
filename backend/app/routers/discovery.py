from fastapi import APIRouter
from ..schemas import DiscoveryResponse, MarketScenario, StrategyMetadata, StrategyParameter
from core.constants import MARKET_SCENARIOS, STRATEGY_METADATA
from core.data.storage import DataStorage
from core.strategies.factory import StrategyFactory
from typing import List

router = APIRouter()

@router.get("/", response_model=DiscoveryResponse)
def get_discovery():
    # 1. Scenarios
    scenarios = [MarketScenario(**s) for s in MARKET_SCENARIOS]
    
    # 2. Strategies with Dynamic Parameters
    strategies = []
    for s_id, s_data in STRATEGY_METADATA.items():
        try:
            # Instantiate strategy to get its schema
            instance = StrategyFactory.get_strategy(s_id, {})
            params = [StrategyParameter(**p) for p in instance.parameters_schema()]
            desc = instance.describe()
        except:
            params = []
            desc = s_data.get("description", "")

        strategies.append(StrategyMetadata(
            id=s_id,
            label=s_data["label"],
            description=desc,
            logic_explanation=s_data.get("logic_explanation", ""),
            risk_profile=s_data.get("risk_profile", "Desconocido"),
            default_params=s_data.get("default_params", {}),
            parameters=params
        ))
    
    # 3. Available Symbols
    storage = DataStorage()
    files = list(storage.base_dir.glob("*.parquet"))
    symbols = set()
    for f in files:
        name = f.stem
        parts = name.split("_")
        if len(parts) >= 2:
            sym = f"{parts[0]}/{parts[1]}"
            symbols.add(sym)
    
    return DiscoveryResponse(
        scenarios=scenarios,
        strategies=strategies,
        available_symbols=list(symbols or ["BTC/USDT"]),
        available_timeframes=["1h", "4h", "1d"]
    )
