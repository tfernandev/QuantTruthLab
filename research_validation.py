import pandas as pd
import numpy as np
import sys
from pathlib import Path
from scipy import stats

# Fix Path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from backend.app.routers.backtest import run_backtest
from backend.app.schemas import BacktestRequest

def run_research_comparison():
    print("\n[RESEARCH] 1. COMPRACION CONTRA RANDOM BASELINE")
    
    scenarios = ["bull_2021", "bear_2022", "etf_2024"]
    results = []

    for sc_id in scenarios:
        # SMA
        res_sma = run_backtest(BacktestRequest(symbol="BTC/USDT", timeframe="1h", strategy_name="SmaCrossover", scenario_id=sc_id))
        # RSI
        res_rsi = run_backtest(BacktestRequest(symbol="BTC/USDT", timeframe="1h", strategy_name="RsiStrategy", scenario_id=sc_id))
        # RANDOM
        res_rand = run_backtest(BacktestRequest(symbol="BTC/USDT", timeframe="1h", strategy_name="RandomStrategy", scenario_id=sc_id, params={"probability": 0.05}))
        
        results.append({
            "Scenario": sc_id,
            "SMA_Ret": res_sma.total_return,
            "RSI_Ret": res_rsi.total_return,
            "RAND_Ret": res_rand.total_return,
            "SMA_Sharpe": res_sma.sharpe_ratio,
            "RSI_Sharpe": res_rsi.sharpe_ratio,
            "RAND_Sharpe": res_rand.sharpe_ratio
        })

    df_res = pd.DataFrame(results)
    print(df_res.to_string())
    return df_res

def run_sensitivity_analysis():
    print("\n[RESEARCH] 2. ANALISIS DE SENSIBILIDAD (SMA)")
    params_list = [
        {"fast_period": 10, "slow_period": 20},
        {"fast_period": 20, "slow_period": 50},
        {"fast_period": 50, "slow_period": 200}
    ]
    
    sens_results = []
    for p in params_list:
        res = run_backtest(BacktestRequest(
            symbol="BTC/USDT", timeframe="1h", strategy_name="SmaCrossover", scenario_id="bull_2021", params=p
        ))
        sens_results.append({
            "Params": f"{p['fast_period']}/{p['slow_period']}",
            "Return": res.total_return,
            "Sharpe": res.sharpe_ratio
        })
    
    df_sens = pd.DataFrame(sens_results)
    print(df_sens.to_string())

def run_statistical_test():
    print("\n[RESEARCH] 3. VALIDACION ESTADISTICA (T-TEST)")
    # We compare the daily returns of SMA vs Random in the ETF 2024 scenario
    sc_id = "etf_2024"
    
    res_sma = run_backtest(BacktestRequest(symbol="BTC/USDT", timeframe="1h", strategy_name="SmaCrossover", scenario_id=sc_id))
    res_rand = run_backtest(BacktestRequest(symbol="BTC/USDT", timeframe="1h", strategy_name="RandomStrategy", scenario_id=sc_id))
    
    # Calculate returns from equity curves
    ret_sma = pd.Series(res_sma.equity_curve).pct_change().dropna()
    ret_rand = pd.Series(res_rand.equity_curve).pct_change().dropna()
    
    t_stat, p_value = stats.ttest_ind(ret_sma, ret_rand)
    
    print(f"Scenario: {sc_id}")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("RESULTADO: Diferencia Significativa (H0 rechazada). Existe evidencia de edge.")
    else:
        print("RESULTADO: No Significativo (H0 no rechazada). El rendimiento es indistinguible del azar.")

if __name__ == "__main__":
    df1 = run_research_comparison()
    df1.to_csv("research_1_comparison.csv")
    
    # Run others and just let them print, but we focus on these
    run_sensitivity_analysis()
    run_statistical_test()
