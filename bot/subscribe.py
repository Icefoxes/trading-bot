import websockets
from okx.websocket import WsUtils
from typing import List
import json
import logging
import asyncio
from bot import TradeBotConf, Strategy, to_tick, to_order, to_bar, to_position, to_balance


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


class ConnectionManager:
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
                'apiKey': conf.apiKey,
                'passphrase': conf.passphrase,
                'secretKey': conf.secretKey,
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

class BalanceSubscribe(ConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'account'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init BalanceSubscribe')
        super().__init__(conf.ws_private, [Subscription(self.channel, {'ccy': 'USDT'})], conf, True)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            balance = to_balance(message['data'][0])
            self.strategy.on_balance_status(balance)
        logging.info(f'[balance] {json.dumps(message)}')

class OrderSubscriber(ConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'orders'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init OrderSubscriber')
        super().__init__(conf.ws_private, [Subscription(self.channel, {'instType': self.strategy.instrumentType})], conf, True)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            orders = to_order(message['data'])
            self.strategy.on_order_status(orders)
        logging.info(f'[order] {json.dumps(message)}')


class PositionSubscriber(ConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'positions'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init PositionSubscriber')
        super().__init__(conf.ws_private, [Subscription(self.channel, {'instType': self.strategy.instrumentType}, interval=3)], conf, True)


    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data'):
            positions = to_position(message['data'])
            self.strategy.on_position_status(positions)
        logging.debug(f'[position] {json.dumps(message)}')
                

class TickSubscriber(ConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.channel = 'tickers'
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init TickSubscriber')
        super().__init__(conf.ws_public, [Subscription(self.channel, {'instId': sub}, interval=1) for sub in self.strategy.instruments])

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel') == self.channel and message.get('data') and len(message.get('data')) > 0:
            ticks = to_tick(message['data'][0])
            self.strategy.on_tick(ticks)
        logging.debug(f'[tick] {json.dumps(message)}')


class BarSubscriber(ConnectionManager):
    def __init__(self, strategy: Strategy) -> None:
        self.bar_types = set([f'candle{bar_type}' for bar_type in strategy.bar_types])
        self.strategy = strategy
        conf = TradeBotConf.load()
        logging.info('init BarSubscriber')
        subscriptions = []
        for instrument in self.strategy.instruments:
            for bar_type in self.bar_types:
                logging.info(f'subscribe {bar_type}-{instrument}')
                subscriptions.append(Subscription(f'{bar_type}', {'instId': instrument}, interval=1))
        
        super().__init__(conf.ws_public, subscriptions)

    async def handle_message(self, message: dict):
        await super().handle_message(message)
        if message.get('arg', {}).get('channel', None) in self.bar_types and message.get('data') and len(message.get('data')) > 0:
            bars = to_bar(message['data'])
            self.strategy.on_bar(bars)
        logging.debug(f'[bar] {json.dumps(message)}')
