from tinydb import TinyDB, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

from typing import List
import logging
from bot import TradeBotConf, ExchangeClient, Balance, Tick, Bar, Order, Position


serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

tick_db = TinyDB('./data/tick.json', storage=serialization)

class Strategy:
    def __init__(self, id: str, instruments: List[str], instrumentType: str, bar_types: List[str]) -> None:
        self.id = id
        self.instruments = instruments
        self.instrumentType = instrumentType
        self.bar_types = bar_types
        self.client = ExchangeClient(TradeBotConf.load())
        self.balance: Balance = None
        # local state
        self.positions = set([])
        self.ticks:List[Tick] = []
        self.bars = {}

    def on_tick(self, ticks: List[Tick]):
        self.ticks.extend(ticks)
        for tick in ticks:
            tick_db.insert(tick._asdict())
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
        for position in positions:
            self.positions.add(position)
        