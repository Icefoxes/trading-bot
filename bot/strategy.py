from typing import List
from datetime import datetime
from collections import namedtuple
import logging

Tick = namedtuple('Tick', ['instrument', 'price', 'timestmap'])

Bar = namedtuple('Bar', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])

Order = namedtuple('Orders', ['orderId', 'orderType', 'instrument', 'instrumentType', 'price', 'mode', 'status', 'side', 'lever', 'timestamp'])

Position = namedtuple('Position', ['positionId','instrument', 'instrumentType', 
                                   'side', 'quantity', 'unrealized_profit', 
                                   'pnl_ratio', 'mode', 'price', 'last','timestamp'])


def to_tick(data: dict) -> List[Tick]:
    ticks = []
    ticks.append(Tick(
        instrument=data['instId'],
        price=float(data['last']),
        timestmap = datetime.fromtimestamp(int(data['ts']) / 1000)
    ))
    return ticks

def to_position(data: List[dict]) -> List[Position]:
    positions = []
    for record in data:
        positions.append(Position(
            positionId=record.get('posId'),
            instrument=record.get('instId'),
            instrumentType=record.get('instType'),
            side=record.get('posSide'),
            quantity=float(record.get('pos')),
            unrealized_profit=round(float(record.get('upl')), 2),
            pnl_ratio = round(float(record.get('uplRatio')) * 100, 2) ,
            mode=record.get('mgnMode'),
            price=float(record.get('avgPx')),
            last=float(record.get('last')),
            timestamp=datetime.fromtimestamp(int(record['cTime']) / 1000)
        ))
    return positions
   

def to_bar(data: List[str]) -> Bar:
    timestamp, open, high, low, close, vol, _, _, _ = data
    return Bar(
        timestamp=datetime.fromtimestamp(int(timestamp) / 1000),
        open=float(open),
        high=float(high),
        low=float(low),
        close=float(close),
        vol=float(vol),
    )


def to_order(records: List[dict]) -> List[Order]:
    orders = []
    for data in records:
        orders.append(Order(
            orderId=data.get('ordId'),
            orderType=data.get('ordType'),
            instrument=data.get('instId'),
            instrumentType=data.get('instType'),
            price=float(data.get('px')),
            mode=data.get('tdMode'),
            status=data.get('state'),
            side=data.get('side'),
            lever=int(data.get('lever')),
            timestamp=datetime.fromtimestamp(int(data.get('cTime')) / 1000)
        ))
    return orders



class Strategy:
    def __init__(self, id: str, instruments: List[str], instrumentType: str, bar_types: List[str]) -> None:
        self.id = id
        self.instruments = instruments
        self.instrumentType = instrumentType
        self.bar_types = bar_types
        # local state
        self.positions = set([])
        self.ticks = []
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

    def on_position_status(self, positions: List[Position]):
        for position in positions:
            self.positions.add(position)
        