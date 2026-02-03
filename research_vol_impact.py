import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Fix Path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from backend.app.routers.backtest import run_backtest
from backend.app.schemas import BacktestRequest

def run_experiment():
    print("RESEARCH EXPERIMENT: IMPACT OF VOLATILITY FILTER")
    print("="*60)
    
    # 1. RSI RAW
    req_raw = BacktestRequest(
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_name="RsiStrategy",
        scenario_id="etf_2024",
        params={"length": 14, "oversold": 30, "overbought": 70}
    )
    res_raw = run_backtest(req_raw)
    
    # 2. RSI + VOLATILITY FILTER
    req_filtered = BacktestRequest(
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_name="EnsembleStrategy",
        scenario_id="etf_2024",
        params={
            "strat_a": "RsiStrategy",
            "strat_b": "VolatilityFilter",
            "operator": "FILTER",
            "params_a": {"length": 14, "oversold": 30, "overbought": 70},
            "params_b": {"threshold_pct": 0.8, "length": 24}
        }
    )
    res_filtered = run_backtest(req_filtered)
    
    print(f"{'Metric':<25} | {'RSI Raw':<15} | {'RSI + Vol Filter':<15}")
    print("-" * 60)
    print(f"{'Total Return %':<25} | {res_raw.total_return:>15.2f} | {res_filtered.total_return:>15.2f}")
    print(f"{'Sharpe Ratio':<25} | {res_raw.sharpe_ratio:>15.2f} | {res_filtered.sharpe_ratio:>15.2f}")
    print(f"{'Total Trades':<25} | {res_raw.total_trades:>15} | {res_filtered.total_trades:>15}")
    print(f"{'P-Value (Honesty)':<25} | {res_raw.p_value:>15.4f} | {res_filtered.p_value:>15.4f}")
    print(f"{'Stability Var %':<25} | {res_raw.stability_variance:>15.2f} | {res_filtered.stability_variance:>15.2f}")
    print("-" * 60)
    
    print("\nRESEARCH CONCLUSIONS:")
    print(f"RSI RAW: {res_raw.research_conclusion}")
    print(f"RSI FILTERED: {res_filtered.research_conclusion}")

if __name__ == "__main__":
    run_experiment()
