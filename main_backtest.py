import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from core.data.storage import DataStorage
from core.strategies.examples import SmaCrossoverStrategy
from core.execution.simulated_broker import SimulatedBroker
from core.core.models import Order, Side, OrderType
from core.analysis.metrics import PerformanceMetrics
from core.utils.logger import logger, setup_logging

def run_backtest(symbol: str = "BTC/USDT", timeframe: str = "1h", initial_capital: float = 10000):
    setup_logging()
    
    # 1. Load Data
    storage = DataStorage()
    df = storage.load_ohlcv(symbol, timeframe)
    
    if df.empty:
        logger.error("No data found. Run main_ingest.py first.")
        return

    logger.info(f"Loaded {len(df)} candles for {symbol}")

    # 2. Run Strategy (Vectorized Signal Generation)
    strategy = SmaCrossoverStrategy("SMA_Cross", params={'fast_period': 20, 'slow_period': 50})
    df_signals = strategy.analyze(df)
    
    # 3. Execution Loop
    broker = SimulatedBroker(initial_capital=initial_capital)
    equity_history = []
    timestamps = []

    # Iterate through candles
    # We use iterrows for simplicity in this demo, but vectorization is preferred for speed in python
    # However, for realistic simulation (path-dependent), iteration is often needed.
    
    logger.info("Starting simulation loop...")
    position_open = False
    
    for timestamps_idx, row in df_signals.iterrows():
        current_price = row['close']
        signal = row['signal'] # 1, -1, 0
        
        # 1. Update Broker State (Check fills)
        broker.process_data_event(symbol, current_price, timestamps_idx)
        
        # 2. Check Signals & Execute
        # Simple Logic: 
        # Signal 1 (Buy) -> If no position, Buy 100% equity.
        # Signal -1 (Sell) -> If position, Sell 100%.
        
        # Note: In a real engine, the strategy would emit a concrete Target Allocate or Order, 
        # not just a raw 1/-1 signal.
        
        holdings = broker.get_positions().get(symbol)
        current_amount = holdings.amount if holdings else 0
        
        if signal == 1 and current_amount == 0:
            # Buy
            # Calculate amount with 99% of cash (leave room for fees)
            cash = broker.cash
            quantity = (cash * 0.99) / current_price
            if quantity > 0.0001:
                order = Order(
                    symbol=symbol,
                    side=Side.BUY,
                    type=OrderType.LIMIT, # Limit at close price to ensure execution logic works
                    price=current_price,
                    amount=quantity
                )
                broker.create_order(order)
                
        elif signal == -1 and current_amount > 0:
            # Sell
            order = Order(
                symbol=symbol,
                side=Side.SELL,
                type=OrderType.LIMIT,
                price=current_price,
                amount=current_amount
            )
            broker.create_order(order)

        # 3. Record Equity
        total_value = broker.cash
        if holdings:
            total_value += holdings.amount * current_price
            
        equity_history.append(total_value)
        timestamps.append(timestamps_idx)

    # 4. Results
    equity_curve = pd.Series(equity_history, index=timestamps)
    metrics = PerformanceMetrics.calculate(equity_curve)
    
    logger.info("Backtest Complete.")
    logger.info("--------------------")
    for k, v in metrics.items():
        logger.info(f"{k}: {v}")
    logger.info("--------------------")
    logger.info(f"Total Trades: {len(broker.trades)}")

    # Optional: Plot
    # plt.figure(figsize=(12, 6))
    # plt.plot(equity_curve, label="Equity")
    # plt.title(f"Backtest {strategy.name} on {symbol}")
    # plt.legend()
    # plt.show() # Blocking if run in script

if __name__ == "__main__":
    run_backtest()
