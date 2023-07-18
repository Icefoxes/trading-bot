from typing import List
import logging
import asyncio
from bot import Balance, Tick, Bar, Order, Position

class Subscriber:
    def run() -> asyncio.Task:
        pass

    def stop():
        pass


class Exchange:
    def get_positions(self) -> List[Position]:
        pass

    def get_balance(self) -> Balance:
        pass

    def place_buy_order(self, instrumentId: str, size: float, price: float) -> Order:
        pass

    def place_sell_order(self, instrumentId: str, size: float, price: float) -> Order:
        pass
    
    def cancel_order(self, orderId: str, instrumentId: str) -> Order:
        pass
    
    def close_position(self, instrumentId: str):
        pass

    # get latest 100 bar
    def get_candlesticks(self, instrumentId: str, bar: str = '1m', limit: int = 100) -> List[Bar]:
        pass

class Strategy:
    def __init__(self, id: str, instruments: List[str], instrumentType: str, bar_types: List[str]) -> None:
        self.id = id
        self.instruments = instruments
        self.instrumentType = instrumentType
        self.bar_types = bar_types
        self.balance: Balance = None
        self.exchange: Exchange = None
        # local state
        self.positions: List[Position] = []
        self.ticks:List[Tick] = []
        self.bars = {}


    def on_tick(self, ticks: List[Tick]):
        self.ticks.extend(ticks)
        if len(self.ticks) % 100 == 0:
            logging.info(f'ticks to {len(self.ticks)}')
        if len(self.ticks) > 10000:
            self.ticks = self.ticks[-5000:]

    def on_bar(self, bars: List[Bar]):
        pass
        
    def on_order_status(self, orders: List[Order]):
        pass

    def on_balance_status(self, balance: Balance):
        self.balance = balance

    def on_position_status(self, positions: List[Position]):
        self.positions.clear()
        self.positions.extend(positions)
