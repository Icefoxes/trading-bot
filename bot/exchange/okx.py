
import asyncio
import websockets
from okx.websocket import WsUtils
import okx.Trade as Trade
import okx.Account as Account
import okx.MarketData as Market

from typing import List
from datetime import datetime
import json
import logging

from bot import TradeBotConf, Strategy, Exchange, Subscriber, Order, Position, Balance, Tick, Bar


class OkxExchangeClient(Exchange):
    def __init__(self,  conf: TradeBotConf) -> None:
        self.conf = {
            'api_key': conf.okx['apiKey'],
            'api_secret_key': conf.okx['secretKey'],
            'domain': conf.okx['domain'],
            'passphrase': conf.okx['passphrase'],
            'flag': '0'
        }
        self.tradeApi = Trade.TradeAPI(**self.conf)
        self.accountApi = Account.AccountAPI(**self.conf)
        self.marketApi = Market.MarketAPI(**self.conf)
    # Account Info
    def get_positions(self) -> List[Position]:
        response = self.accountApi.get_positions()
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_okx_position(response['data']) 
        return []

    def get_balance(self):
        return self.accountApi.get_account_balance()
    # Trade Info
    def get_orders(self) -> List[Order]:
        response = self.tradeApi.get_order_list()
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_okx_order(response['data']) 
        return []
    
    def place_buy_order(self, symbol: str, size: float, price: float):
        return self.tradeApi.place_order(instId=symbol, tdMode='isolated', side='buy', sz=str(size), px=str(price), ordType='post_only')
    
    def place_sell_order(self, symbol: str, size: float, price: float):
        return self.tradeApi.place_order(instId=symbol, tdMode='isolated', side='sell', sz=str(size), px=str(price), ordType='post_only')
    
    def cancel_order(self, orderId: str, symbol: str):
        return self.tradeApi.cancel_order(instId=symbol, ordId=orderId)
    
    def close_position(self, symbol: str):
        return self.tradeApi.close_positions(instId=symbol, mgnMode='isolated')

    # get latest 100 bar
    def get_candlesticks(self, symbol: str, bar: str = '1m', limit: int = 100) -> List[Bar]:
        response = self.marketApi.get_candlesticks(instId=symbol, bar=bar, limit=str(limit))
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_okx_bar(response['data']) 
        return []
    

def to_okx_tick(data: dict) -> List[Tick]:
    ticks = []
    ticks.append(Tick(
        symbol=data['instId'],
        price=float(data['last']),
        timestmap = datetime.fromtimestamp(int(data['ts']) / 1000)
    ))
    return ticks


def to_okx_position(data: List[dict]) -> List[Position]:
    positions = []
    for record in data:
        positions.append(Position(
            symbol=record.get('instId'),
            instrumentType=record.get('instType'),
            side=record.get('posSide'),
            quantity=float(record.get('pos')),
            unrealized_profit=round(float(record.get('upl')), 2),
            unrealized_profit_ratio = round(float(record.get('uplRatio')) * 100, 2) ,
            mode=record.get('mgnMode'),
            price=float(record.get('avgPx')),
            timestamp=datetime.fromtimestamp(int(record['cTime']) / 1000)
        ))
    return positions
   

def to_okx_bar(records: List[str]) -> List[Bar]:
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


def to_okx_order(records: List[dict]) -> List[Order]:
    orders = []
    for data in records:
        orders.append(Order(
            orderId=data.get('ordId'),
            orderType=data.get('ordType'),
            symbol=data.get('instId'),
            instrumentType=data.get('instType'),
            price=float(data.get('px')),
            status=data.get('state'),
            side=data.get('side'),
            quantity=0,
            timestamp=datetime.fromtimestamp(int(data.get('cTime')) / 1000)
        ))
    return orders


def to_okx_balance(records: dict) -> List[Balance]:
    balance = []
    if 'details' in records:
        for record in records['details']:
            if float(record.get('availBal')) != 0:
                balance.append(Balance(asset=record['ccy'], availableBalance=float(record.get('availBal'))))
    return balance


class Subscription:
    def __init__(self, channel: str, arg: dict, interval: int = 0) -> None:
        self.channel = channel
        self.arg = {
            'channel': channel,
            "extraParams": "{\"updateInterval\": INTERVAL}".replace('INTERVAL', str(interval)),
            **arg
        }

    def __repr__(self) -> str:
        return self.arg


class OkxConnectionManager:
    def __init__(self,
                 uri: str,
                 subscriptions: List[Subscription],
                 conf: TradeBotConf = None,
                 private: bool = False) -> None:
        self.uri = uri
        self.subscriptions = subscriptions
        self.private = private
        if private and conf:
            self.conf = {
                'apiKey': conf.okx['apiKey'],
                'passphrase': conf.okx['passphrase'],
                'secretKey': conf.okx['secretKey'],
                'useServerTime': False
            }

    async def run(self):
        async for conn in websockets.connect(self.uri):
            try:
                # login
                if self.private and self.conf:
                    payload = WsUtils.initLoginParams(**self.conf)
                    await conn.send(payload.decode())
                    await asyncio.sleep(3)
                # subscribe
                for sub in self.subscriptions:
                    await conn.send(json.dumps({
                        'op': 'subscribe',
                        'args': [sub.arg]
                    }))
                async for message in conn:
                    await self.handle_message(json.loads(message))
            except websockets.ConnectionClosed:
                logging.error(f"{','.join([sub.channel for sub in self.subscriptions])} reconnecting")
                continue
  
    async def handle_message(self, message: dict):
        if message.get('event'):
            logging.info(f"{','.join([sub.channel for sub in self.subscriptions])} {json.dumps(message)}")


class BalanceSubscribe(OkxConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'account'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init BalanceSubscribe')
        super().__init__(conf.okx['ws_private'], [Subscription(self.channel, {'ccy': 'USDT'})], conf, True)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            balance = to_okx_balance(message['data'][0])
            self.strategy.on_balance_status(balance)
        logging.info(f'[balance] {json.dumps(message)}')


class OrderSubscriber(OkxConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'orders'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init OrderSubscriber')
        super().__init__(conf.okx['ws_private'], [Subscription(self.channel, {'instType': self.strategy.instrumentType})], conf, True)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            orders = to_okx_order(message['data'])
            self.strategy.on_order_status(orders)
        logging.info(f'[order] {json.dumps(message)}')


class PositionSubscriber(OkxConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'positions'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init PositionSubscriber')
        super().__init__(conf.okx['ws_private'], [Subscription(self.channel, {'instType': self.strategy.instrumentType}, interval=3)], conf, True)


    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            positions = to_okx_position(message['data'])
            self.strategy.on_position_status(positions)
        logging.debug(f'[position] {json.dumps(message)}')


class TickSubscriber(OkxConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'tickers'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init TickSubscriber')
        super().__init__(conf.okx['ws_public'], [Subscription(self.channel, {'instId': sub}, interval=1) for sub in self.strategy.symbols])

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data') and len(message.get('data')) > 0:
            ticks = to_okx_tick(message['data'][0])
            self.strategy.on_tick(ticks)
        logging.debug(f'[tick] {json.dumps(message)}')


class BarSubscriber(OkxConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.bar_types = set([f'candle{bar_type}' for bar_type in strategy.klines])
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init BarSubscriber')
        subscriptions = []
        for symbol in self.strategy.symbols:
            for bar_type in self.bar_types:
                logging.info(f'subscribe {bar_type}-{symbol}')
                subscriptions.append(Subscription(f'{bar_type}', {'instId': symbol}, interval=1))
        
        super().__init__(conf.okx['ws_public'], subscriptions)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel', None) in self.bar_types and message.get('data') and len(message.get('data')) > 0:
            bars = to_okx_bar(message['data'])
            self.strategy.on_bar(bars)
        logging.debug(f'[bar] {json.dumps(message)}')


class OkxSubscriber(Subscriber):
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy
        self.strategy.on_init_exchange(OkxExchangeClient(TradeBotConf.load()))
    
    
    def run(self) -> List[asyncio.Future]:
        return asyncio.gather(BalanceSubscribe(self.strategy).run(),
                            OrderSubscriber(self.strategy).run(),
                            BarSubscriber(self.strategy).run(),
                            TickSubscriber(self.strategy).run(),
                            PositionSubscriber(self.strategy).run())
