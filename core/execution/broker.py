from abc import ABC, abstractmethod
from typing import List, Dict
from core.core.models import Order, Position, Trade

class Broker(ABC):
    @abstractmethod
    def get_balance(self) -> Dict[str, float]:
        """Returns map of asset -> free amount"""
        pass

    @abstractmethod
    def get_positions(self) -> Dict[str, Position]:
        pass
    
    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        pass
