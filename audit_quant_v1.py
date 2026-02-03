import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Fix Path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from core.data.storage import DataStorage
from core.strategies.examples import SmaCrossoverStrategy
from core.execution.simulated_broker import SimulatedBroker
from core.analysis.metrics import PerformanceMetrics
from core.core.models import Order, Side, OrderType

def audit_data():
    print("\n--- 1. AUDITORÍA DE DATOS ---")
    storage = DataStorage()
    df = storage.load_ohlcv("BTC/USDT", "1h")
    
    # Order and duplicates
    is_ordered = df.index.is_monotonic_increasing
    duplicates = df.index.duplicated().sum()
    
    # Gaps
    diffs = pd.Series(df.index).diff().dropna()
    expected_diff = pd.Timedelta(hours=1)
    gaps = (diffs != expected_diff).sum()
    
    print(f"Total filas: {len(df)}")
    print(f"Orden cronológico: {'OK' if is_ordered else 'FALLA'}")
    print(f"Duplicados: {duplicates}")
    print(f"Huecos detectados (gaps > 1h): {gaps}")
    
    if gaps > 0:
        biggest_gap = diffs.max()
        print(f"Mayor hueco: {biggest_gap}")

def audit_strategy_execution_bug():
    print("\n--- 2. AUDITORÍA DE EJECUCIÓN (RSI vs SMA) ---")
    storage = DataStorage()
    df = storage.load_ohlcv("BTC/USDT", "1h")
    df = df.tail(1000) # Sample
    
    from backend.app.routers.backtest import run_backtest
    from backend.app.schemas import BacktestRequest
    
    # Simulate SMA
    req_sma = BacktestRequest(
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_name="SmaCrossover",
        params={"fast_period": 10, "slow_period": 20}
    )
    res_sma = run_backtest(req_sma)
    
    # Simulate RSI (currently should fallback to SMA in backtest.py)
    req_rsi = BacktestRequest(
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_name="RsiStrategy",
        params={"length": 14}
    )
    res_rsi = run_backtest(req_rsi)
    
    print(f"SMA Return: {res_sma.total_return}% | Trades: {res_sma.total_trades}")
    print(f"RSI Return: {res_rsi.total_return}% | Trades: {res_rsi.total_trades}")
    
    if res_sma.total_return == res_rsi.total_return and res_sma.total_trades == res_rsi.total_trades:
        print("CRÍTICO: Inconsistencia detectada. RSI está produciendo los mismos resultados que SMA.")
        print("RAZÓN POSIBLE: El router backtest.py no tiene implementada la lógica para RsiStrategy.")

def audit_lookahead_bias():
    print("\n--- 3. AUDITORÍA DE LOOKAHEAD BIAS ---")
    # In backtest.py:
    # for timestamp, row in df_signals.iterrows():
    #     signal = int(row.get('signal', 0))
    #     broker.process_data_event(..., price=row['close'])
    #     ...
    #     order = Order(..., price=row['close'])
    #     broker._execute_fill(order, price=row['close'])
    
    print("HALLAZGO: Lookahead Bias detectado en backend/app/routers/backtest.py")
    print("Explicación: La señal generada en la vela T se ejecuta al precio de cierre de la vela T.")
    print("En la vida real, solo conoces el cierre de T al final de la vela. La ejecución debe ser en T+1.")

if __name__ == "__main__":
    audit_data()
    audit_strategy_execution_bug()
    audit_lookahead_bias()
