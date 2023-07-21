import asyncio
from typing import List
from enum import Enum
import logging

from bot import Balance, Tick, Bar, Order, Position, Trade

class ExchangeEnum(Enum):
    OKX = 1
    Binance = 2


class Exchange:
    def get_positions(self) -> List[Position]:
        pass

    def get_balance(self) -> Balance:
        pass

    def get_orders(self) -> List[Order]:
        pass

    def place_buy_order(self, symbol: str, size: float, price: float) -> Order:
        pass

    def place_sell_order(self, symbol: str, size: float, price: float) -> Order:
        pass
    
    def cancel_order(self, orderId: str, symbol: str) -> Order:
        pass
    
    def close_position(self, symbol: str):
        pass

    # get latest 100 bar
    def get_candlesticks(self, symbol: str, bar: str = '1m', limit: int = 100) -> List[Bar]:
        pass

    def get_trades(self, symbol: str) -> List[Trade]:
        pass

class Subscriber:
    def run(self) -> asyncio.Task:
        pass

    def stop(self):
        pass


class Strategy:
    def __init__(self, id: str, symbols: List[str], instrumentType: str, klines: List[str]) -> None:
        self.id = id
        self.symbols = symbols
        self.instrumentType = instrumentType
        self.klines = klines
        self.balance: List[Balance] = []
        self.exchange: Exchange = None
        # local state
        self.positions: List[Position] = []
        self.ticks:List[Tick] = []
        self.bars = {}

    def on_init_exchange(self, exchange: Exchange):
        self.exchange = exchange
        
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

    def on_balance_status(self, balance: List[Balance]):
        self.balance.clear()
        self.balance.extend(balance)

    def on_position_status(self, positions: List[Position]):
        self.positions.clear()
        self.positions.extend(positions)
