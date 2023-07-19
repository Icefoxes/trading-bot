from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
import schedule

import asyncio
from datetime import datetime
from typing import List
import time
import logging

from bot import TradeBotConf, Strategy, Subscriber, Exchange,  Order, Position, Balance, Tick, Bar

class BinanceUMExchangeClient(Exchange):
    def __init__(self,  conf: TradeBotConf) -> None:
        self.conf = {
            'key': conf.binance['apiKey'],
            'secret': conf.binance['secretKey']
        }
        self.client = UMFutures(**self.conf)
       
    # Account Info
    def get_positions(self) -> List[Position]:
        response: List[Position] = []
        for pos in self.client.account()['positions']:
            if float(pos['positionAmt']) > 0:
                response.append(Position(
                    symbol=pos['symbol'],
                    instrumentType='SWAP',
                    side=pos['positionSide'],
                    quantity=float(pos['positionAmt']),
                    unrealized_profit=round(float(pos['unrealizedProfit']), 3),
                    pnl_ratio = round(float(pos['unrealizedProfit']) / float(pos['initialMargin'])) * 100,
                    mode='isolated' if pos['isolated'] else 'cross',
                    price=float(pos['entryPrice']),
                    last=0,
                    timestamp=datetime.fromtimestamp(int(pos['updateTime'] / 1000))
                ))
        return response

    def get_balance(self):
        response: List[Balance] = []
        for record in self.client.balance(recvWindow=6000):
            if float(record['availableBalance']) != 0:
                response.append(Balance(asset=record['asset'], availableBalance=float(record['availableBalance'])))
        return response

    
    def place_buy_order(self, symbol: str, size: float, price: float):
        params = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': size,
            'price': price
        }
        return self.client.new_order(**params)
    
    def place_sell_order(self, symbol: str, size: float, price: float):
        params = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': size,
            'price': price
        }
        return self.client.new_order(**params)
    
    def cancel_order(self, orderId: str, symbol: str):
        return self.client.cancel_order(symbol=symbol, orderId=int(orderId))
    
    def close_position(self, symbol: str):
        pass

    # get latest 100 bar
    def get_candlesticks(self, symbol: str, bar: str = '1m', limit: int = 100) -> List[Bar]:
        bars =[]
        for bar in self.client.klines(symbol=symbol, interval=bar, limit=limit):
            _stamp, _open, _high, _low, _close, _vol, *_ = bar
            bars.append(Bar(
                timestamp=datetime.fromtimestamp(_stamp / 1000),
                open=float(_open),
                high=float(_high),
                low=float(_low),
                close=float(_close),
                vol=float(_vol)
            ))
        return bars
       

class BinanceUMSubscriber(Subscriber):
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy
        self.strategy.on_init_exchange(BinanceUMExchangeClient(TradeBotConf.load()))
        conf = TradeBotConf.load()
        self.conf = {
            'key': conf.binance['apiKey'],
            'secret': conf.binance['secretKey']
        }
        self.listenKey: str = None
        self.last_auth: datetime = datetime.utcnow()
        self.last_tick: int = None
        self.last_bar : int = None
        
    
    def renew(self):
        logging.info('renew key')
        if self.listenKey:
            self.client.renew_listen_key(self.listenKey)
    
    def _run(self):
        self.client = UMFutures(**self.conf)
        self.listenKey = self.client.new_listen_key()['listenKey']
        self.ws = UMFuturesWebsocketClient()
        idx = 1
        for symbol in self.strategy.symbols:
            self.ws.mini_ticker(id=idx, callback=self.handle_message, symbol=symbol)
            idx += 1
        for symbol in self.strategy.symbols:
            for bar_type in self.strategy.klines:
                self.ws.kline(id=idx, callback=self.handle_message, symbol=symbol, interval=bar_type)
                idx += 1
        self.ws.user_data(listen_key=self.listenKey, id=idx+1, callback=self.handle_message)
        self.ws.run()

    def run(self) -> asyncio.Task:
        return asyncio.create_task(self._run())
    
    def stop(self):
        self.ws.stop()

    def handle_message(self, data: dict):
        if (datetime.utcnow() - self.last_auth).seconds > 60 * 45:
            self.renew()
            self.last_auth = datetime.utcnow()
        event = data.get('e')
        msg_stamp = data.get('E')
        
        if not event:
            return
        elif '24hrMiniTicker' == event:
            if not self.last_tick or msg_stamp - self.last_tick >= 1000:
                tick = Tick(symbol=data.get('s'), price=round(float(data.get('c')), 4), timestmap=datetime.fromtimestamp(int(msg_stamp / 1000)))
                self.strategy.on_tick([tick])
            self.last_tick = msg_stamp
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
                symbol=record.get('s'),
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
            # handle positions
            positions: List[Position] = []
            for _position in record.get('P'):
                if float(_position['iw']) > 0:
                    positions.append(Position(
                        symbol=_position.get('s'),
                        instrumentType='SWAP',
                        side=_position.get('ps'),
                        quantity=float(_position['pa']),
                        unrealized_profit=round(float(_position['up']), 3),
                        pnl_ratio = round(float(_position['up']) / float(_position['iw']) * 100, 3),
                        mode=_position.get('mt'),                    
                        price=float(_position['ep']),            # entry price
                        last=0,
                        timestamp=datetime.fromtimestamp(int(msg_stamp / 1000))
                    ))
            self.strategy.on_position_status(positions)
            # handle balance
            balance: List[Balance] = []
            for record in record.get('B'):
                balance.append(Balance(
                    asset=record['a'],                                # asset
                    availableBalance=round(float(record['bc']), 2),   # balance
                ))
            if len(balance) > 0:
                self.strategy.on_balance_status(balance)
        elif 'kline' == event:
            if not self.last_bar or msg_stamp - self.last_bar >= 1000: 
                record = data.get('k', {})
                bar = Bar(
                    timestamp=datetime.fromtimestamp(int(msg_stamp) / 1000),
                    open=float(record['o']),
                    high=float(record['h']),
                    low=float(record['l']),
                    close=float(record['c']),
                    vol=float(record['q']),
                )
                self.strategy.on_bar([bar])
            self.last_bar = msg_stamp