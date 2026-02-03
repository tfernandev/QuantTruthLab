from typing import Dict, List
from datetime import datetime
from core.execution.broker import Broker
from core.core.models import Order, Position, Trade, OrderStatus, Side, OrderType
from core.config import settings
from core.utils.logger import logger

class SimulatedBroker(Broker):
    """
    Simulates an exchange. 
    Keeps track of:
    - Cash balance
    - Asset holdings
    - Active orders
    """
    def __init__(self, initial_capital: float = settings.INITIAL_CAPITAL):
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        self.trades: List[Trade] = []
        self.maker_fee = settings.MAKER_FEE
        self.taker_fee = settings.TAKER_FEE
        
        logger.info(f"SimulatedBroker initialized with ${initial_capital}")

    def get_balance(self) -> Dict[str, float]:
        return {"USDT": self.cash}

    def get_positions(self) -> Dict[str, Position]:
        return self.positions

    def create_order(self, order: Order) -> Order:
        logger.info(f"Order received: {order.side} {order.amount} {order.symbol}")
        # Basic validation
        cost = order.amount * (order.price if order.price else 0) 
        # In simulation, we might not know price for market orders yet, 
        # so validation happens at execution time or we estimate.
        
        self.orders[order.id] = order
        return order

    def cancel_order(self, order_id: str) -> bool:
        if order_id in self.orders:
            self.orders[order_id].status = OrderStatus.CANCELED
            return True
        return False

    def process_data_event(self, symbol: str, current_price: float, timestamp: datetime):
        """
        Core of the simulation: Check if pending orders can be filled.
        This would be called for every new candle or tick.
        """
        # Update positions mark-to-market
        if symbol in self.positions:
            self.positions[symbol].update(current_price)

        # Match orders
        for order_id, order in list(self.orders.items()):
            if order.status != OrderStatus.PENDING:
                continue
            
            if order.symbol != symbol:
                continue
                
            # Simulate Fill
            should_fill = False
            fill_price = current_price
            
            if order.type == OrderType.MARKET:
                should_fill = True
                # Slippage could be added here
            elif order.type == OrderType.LIMIT:
                if order.side == Side.BUY and current_price <= order.price:
                    should_fill = True
                    fill_price = order.price # Optimistic fill or current_price? Conservative is order.price
                elif order.side == Side.SELL and current_price >= order.price:
                    should_fill = True
                    fill_price = order.price
            
            if should_fill:
                self._execute_fill(order, fill_price, timestamp)

    def _execute_fill(self, order: Order, price: float, timestamp: datetime):
        # Calculate cost and fee
        cost = order.amount * price
        fee = cost * self.taker_fee # Simplify to taker for now
        
        # Check funds (for BUY)
        if order.side == Side.BUY:
            total_deduction = cost + fee
            if self.cash < total_deduction:
                logger.warning(f"Order {order.id} rejected: Insufficient funds")
                order.status = OrderStatus.REJECTED
                return
            
            self.cash -= total_deduction
            self._update_position(order.symbol, order.amount, price)
            
        # Check holdings (for SELL)
        elif order.side == Side.SELL:
            # position check
            pos = self.positions.get(order.symbol)
            if not pos or pos.amount < order.amount:
                 logger.warning(f"Order {order.id} rejected: Insufficient assets")
                 order.status = OrderStatus.REJECTED
                 return
                 
            self.cash += (cost - fee)
            self._update_position(order.symbol, -order.amount, price)

        # Create Trade Record
        trade = Trade(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            amount=order.amount,
            price=price,
            cost=cost,
            fee=fee,
            timestamp=timestamp
        )
        self.trades.append(trade)
        
        order.status = OrderStatus.FILLED
        order.updated_at = timestamp
        logger.info(f"FILLED: {order.side} {order.amount} {order.symbol} @ {price}")

    def _update_position(self, symbol: str, amount_delta: float, price: float):
        pos = self.positions.get(symbol, Position(symbol=symbol))
        
        # Weighted Average Entry Price logic (simplified)
        if amount_delta > 0: # Buying
            new_amount = pos.amount + amount_delta
            total_cost = (pos.amount * pos.average_entry_price) + (amount_delta * price)
            pos.average_entry_price = total_cost / new_amount
            pos.amount = new_amount
        else: # Selling
            # Entry price doesn't change when selling, only amount
            pos.amount += amount_delta
            if pos.amount <= 0.00000001: # Close enough to zero
                pos.amount = 0
                pos.average_entry_price = 0
        
        self.positions[symbol] = pos
