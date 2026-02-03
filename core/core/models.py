from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderStatus(str, Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    side: Side
    type: OrderType
    amount: float
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Trade(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    symbol: str
    side: Side
    amount: float
    price: float
    cost: float # amount * price
    fee: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Position(BaseModel):
    symbol: str
    amount: float = 0.0
    average_entry_price: float = 0.0
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    
    def update(self, last_price: float):
        self.current_price = last_price
        if self.amount == 0:
            self.unrealized_pnl = 0
            return
            
        diff = self.current_price - self.average_entry_price
        self.unrealized_pnl = diff * self.amount
