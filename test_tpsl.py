import requests
import json

API_URL = "http://localhost:8000/api/backtest/run/"

def test_tpsl():
    print("--- TEST BOOTSTRAP: TP/SL Feature ---")
    
    # 1. Base Run (No TP/SL)
    payload_base = {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "strategy_name": "SmaCrossover",
        "scenario_id": "bull_2021",
        "initial_capital": 10000,
        "params": {"fast_period": 10, "slow_period": 50}
    }
    print("Running BASE simulation...")
    r = requests.post(API_URL, json=payload_base)
    if r.status_code == 200:
        base_res = r.json()
        print(f"Base Ret: {base_res['total_return']:.2f}% | Trades: {base_res['total_trades']}")
    else:
        print(f"Base Error: {r.text}")
        return

    # 2. Run with STRICT TP/SL (Should reduce Drawdown but maybe Return too)
    # SL 5%, TP 10%
    payload_tpsl = payload_base.copy()
    payload_tpsl.update({
        "tp_type": "percent",
        "tp_value": 10.0,
        "sl_type": "percent",
        "sl_value": 5.0
    })
    
    print("\nRunning TP/SL simulation (SL=5%, TP=10%)...")
    r2 = requests.post(API_URL, json=payload_tpsl)
    if r2.status_code == 200:
        tpsl_res = r2.json()
        print(f"TP/SL Ret: {tpsl_res['total_return']:.2f}% | Trades: {tpsl_res['total_trades']}")
        print(f"Metrics (New):")
        print(f"  Max Latent DD: {tpsl_res['max_latent_drawdown']:.2f}%")
        print(f"  Time in Market: {tpsl_res['time_in_market_pct']:.2f}%")
        print(f"  Time in Loss: {tpsl_res['time_in_loss_pct']:.2f}%")
        print(f"  Avg Duration: {tpsl_res['avg_trade_duration_candles']:.1f} hours")
        
        if tpsl_res['total_trades'] > base_res['total_trades']:
             print("[OK] More trades due to TP/SL exits (likely).")
        else:
             print("[INFO] Trades count similar or lower (depends on trend).")
             
    else:
        print(f"TP/SL Error: {r2.text}")

if __name__ == "__main__":
    test_tpsl()
