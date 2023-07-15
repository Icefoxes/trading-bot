from datetime import datetime
import pandas as pd
import json
from typing import List
from bot import Messager, Strategy, Order, Tick
from bot.strategy import Position


class NotificationStrategy(Strategy):
    def __init__(self, messager: Messager) -> None:
        super().__init__(id='a4e16024-ec4c-42f6-a6ad-845419df0788', 
                         instruments=['BTC-USDT-SWAP'],
                         instrumentType='SWAP', 
                         bar_types=['1m'])
        self.messager = messager
        self.last_notify = datetime.now()

    def on_order_status(self, orders: List[Order]):
        for order in orders:
            self.messager.notify(f'{json.dumps(order._asdict(), default=str)}')

    def on_position_status(self, positions: List[Position]):
        super().on_position_status(positions)
        for pos in positions:
            if pos.pnl_ratio < -20:
                self.messager.notify_with_interval(f'{json.dumps(pos._asdict(), default=str)}')

    def on_tick(self, tick: Tick):
        super().on_tick(tick)
        sample = [tick._asdict() for tick in self.ticks[-200:]]
        df = pd.DataFrame(sample)
        if df.price.std() > 5 and (datetime.now() - self.last_notify).seconds >= 5 * 60:
            self.last_notify = datetime.now()
            self.messager.notify_with_interval(f'price rapid change, current = {sample[-1]["price"]}')
