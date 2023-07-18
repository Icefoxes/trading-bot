from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
import schedule
import asyncio

from datetime import datetime
import time
import json
import logging

from bot import TradeBotConf, Strategy, Subscriber,  Order, Position, Balance, Tick, Bar


class BinanceUMSubscriber(Subscriber):
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy
        conf = TradeBotConf.load()
        self.conf = {
            'key': conf.binance['apiKey'],
            'secret': conf.binance['secretKey']
        }
        schedule.every(45).minutes.do(self.renew)
    
    def renew(self):
        logging.info('renew key')
        self.client.renew_listen_key(self.listenKey)
    
    def _run(self):
        self.client = UMFutures(**self.conf)
        self.listenKey = self.client.new_listen_key()['listenKey']
        self.ws = UMFuturesWebsocketClient()
        idx = 1
        for symbol in self.strategy.instruments:
            self.ws.mini_ticker(id=idx, callback=self.handle_message, symbol=symbol)
            idx += 1
        for symbol in self.strategy.instruments:
            for bar_type in self.strategy.bar_types:
                self.ws.kline(id=idx, callback=self.handle_message, symbol=symbol, interval=bar_type)
                idx += 1
        self.ws.user_data(listen_key=self.listenKey, id=idx+1, callback=self.handle_message)

        self.ws.run()
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self) -> asyncio.Task:
        return asyncio.create_task(self._run())
    
    def stop(self):
        self.ws.stop()

    def handle_message(self, message: str):
        data = json.loads(message)
        event = data.get('e')
        if not event:
            return
        elif '24hrMiniTicker' == event:
            tick = Tick(instrument=data.get('s'), price=round(float(data.get('c')), 4), timestmap=datetime.fromtimestamp(int(data.get('E') / 1000)))
            self.strategy.on_tick([tick])
        elif 'ORDER_TRADE_UPDATE' == event:
            record = data.get('o', {})
            order = Order(
                orderId=record.get('i'),
                # MARKET
                # LIMIT
                # STOP
                # TAKE_PROFIT
                # LIQUIDATION
                orderType=record.get('o'),
                instrument=record.get('s'),
                instrumentType='SWAP',
                price=float(record.get('ap')),
                mode='mode',
                # NEW
                # CANCELED
                # CALCULATED
                # EXPIRED
                # TRADE
                # AMENDMENT
                status=record.get('x'),
                # BUY || SELL
                side=record.get('S'),
                lever=0,
                qty=float(record.get('q')),
                timestamp=datetime.fromtimestamp(int(record.get('T')) / 1000)
            )
            self.strategy.on_order_status([order])
        elif 'ACCOUNT_UPDATE' == event:
            record = data.get('a', {})
            _positions = record.get('P')
            positions = []
            for _position in _positions:
                positions.append(Position(
                    positionId='',
                    instrument=_position.get('s'),
                    instrumentType='SWAP',
                    side=_position.get('ps'),
                    quantity=float(_position.get('pa')),
                    unrealized_profit=round(float(_position.get('up')), 2),
                    pnl_ratio = 0,
                    mode=_position.get('mt'),
                    price=float(_position.get('ep')),
                    last=0,
                    timestamp=datetime.fromtimestamp(int(data['E']) / 1000)
                ))
            self.strategy.on_position_status(positions)

            _balances = record.get('B')
            for _balance in _balances:
                if _balance.get('a') == 'USDT':
                    balance = Balance(
                        availableBalance=round(float(_balance.get('wb')), 2),
                        frozenBalance=0
                    )
                    self.strategy.on_balance_status(balance)
        elif 'kline' == event:
            record = data.get('k', {})
            bar = Bar(
                timestamp=datetime.fromtimestamp(int(data['E']) / 1000),
                open=float(record['o']),
                high=float(record['h']),
                low=float(record['l']),
                close=float(record['c']),
                vol=float(record['q']),
            )
            self.strategy.on_bar([bar])