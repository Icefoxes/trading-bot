import pandas as pd
import json
from typing import List
from bot import Messager, Strategy, Order, Tick, Position


class NotificationStrategy(Strategy):
    def __init__(self, messager: Messager) -> None:
        super().__init__(id='a4e16024-ec4c-42f6-a6ad-845419df0788', 
                         # Binance is BTCUSDT
                         # OKX is BTC-USDT-SWAP
                         symbols=['BTCUSDT'],
                         instrumentType='SWAP', 
                         klines=['1m'])
        self.messager = messager

    def on_order_status(self, orders: List[Order]):
        for order in orders:
            self.messager.notify(f'{json.dumps(order._asdict(), default=str)}')

    def on_position_status(self, positions: List[Position]):
        super().on_position_status(positions)
        for pos in positions:
            if pos.pnl_ratio < -20:
                self.messager.notify_with_interval(f'{json.dumps(pos._asdict(), default=str)}')

    def on_tick(self, ticks: List[Tick]):
        super().on_tick(ticks)
        sample = [tick._asdict() for tick in self.ticks[-200:]]
        df = pd.DataFrame(sample)
        if df.price.std() > 15:
            self.messager.notify_with_interval(f'price rapid change, current = {sample[-1]["price"]}')
