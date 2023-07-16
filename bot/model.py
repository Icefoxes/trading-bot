from typing import List
from datetime import datetime
from collections import namedtuple

Tick = namedtuple('Tick', ['instrument', 'price', 'timestmap'])

Bar = namedtuple('Bar', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])

Order = namedtuple('Orders', ['orderId', 'orderType', 'instrument', 'instrumentType', 'price', 'mode', 'status', 'side', 'lever', 'timestamp'])

Position = namedtuple('Position', ['positionId','instrument', 'instrumentType', 
                                   'side', 'quantity', 'unrealized_profit', 
                                   'pnl_ratio', 'mode', 'price', 'last','timestamp'])

Balance = namedtuple('Balance',['frozenBalance', 'availableBalance'])

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
   

def to_bar(records: List[str]) -> List[Bar]:
    bars: List[Bar] = []
    for record in records:
        timestamp, open, high, low, close, vol, _, _, _ = record
        bars.append(Bar(
            timestamp=datetime.fromtimestamp(int(timestamp) / 1000),
            open=float(open),
            high=float(high),
            low=float(low),
            close=float(close),
            vol=float(vol),
        )) 
    return bars


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

def to_balance(records: dict) -> Balance:
    if 'details' in records:
        for record in records['details']:
            if record['ccy'] == 'USDT':
                return Balance(availableBalance=float(record.get('availBal')), frozenBalance=float(record.get('frozenBal')))