import pytest
from core.execution.simulated_broker import SimulatedBroker
from core.core.models import Order, OrderType, Side

def test_broker_initialization():
    broker = SimulatedBroker(initial_capital=10000.0)
    assert broker.cash == 10000.0
    assert len(broker.positions) == 0

def test_broker_buy_execution():
    broker = SimulatedBroker(initial_capital=10000.0)
    
    # 1. Market Data Update
    timestamp = 1625097600
    price_btc = 35000.0
    broker.process_data_event("BTC/USDT", price_btc, timestamp)
    
    # 2. Place Buy Order
    # Buy 0.1 BTC -> Cost ~3500. Comm 0.1% -> 3.5
    qty = 0.1
    order = Order(symbol="BTC/USDT", side=Side.BUY, type=OrderType.MARKET, amount=qty, price=price_btc)
    broker.create_order(order)
    
    # 3. Simulate Fill (The broker usually fills on next event or via internal method in backtest loop)
    # Here we manually trigger the fill logic as used in the backtest loop
    broker._execute_fill(order, price_btc, timestamp)
    
    # 4. Check State
    pos = broker.get_positions().get("BTC/USDT")
    assert pos is not None
    assert pos.amount == 0.1
    assert pos.average_entry_price == 35000.0
    
    # Cash should be: 10000 - (35000 * 0.1) - commission
    # Commission = 3500 * 0.001 = 3.5
    expected_cash = 10000.0 - 3500.0 - 3.5
    assert abs(broker.cash - expected_cash) < 1e-5

def test_broker_sell_execution():
    broker = SimulatedBroker(initial_capital=10000.0)
    timestamp = 1625097600
    price_btc = 35000.0
    broker.process_data_event("BTC/USDT", price_btc, timestamp)
    
    # Setup initial position
    buy_order = Order(symbol="BTC/USDT", side=Side.BUY, type=OrderType.MARKET, amount=0.1, price=price_btc)
    broker.create_order(buy_order)
    broker._execute_fill(buy_order, price_btc, timestamp)
    
    initial_cash_after_buy = broker.cash
    
    # Sell 0.05 BTC at 40000
    new_price = 40000.0
    broker.process_data_event("BTC/USDT", new_price, timestamp + 3600)
    
    sell_order = Order(symbol="BTC/USDT", side=Side.SELL, type=OrderType.MARKET, amount=0.05, price=new_price)
    broker.create_order(sell_order)
    broker._execute_fill(sell_order, new_price, timestamp + 3600)
    
    # Check new position
    pos = broker.get_positions().get("BTC/USDT")
    assert abs(pos.amount - 0.05) < 1e-9
    
    # Check Cash
    # Proceeds = 0.05 * 40000 = 2000
    # Comm = 2000 * 0.001 = 2.0
    expected_cash = initial_cash_after_buy + 2000.0 - 2.0
    assert abs(broker.cash - expected_cash) < 1e-5
