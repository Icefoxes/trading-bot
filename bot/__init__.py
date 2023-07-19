import logging

from bot.config import TradeBotConf
from bot.messager import Messager
from bot.model import Order, Position, Tick, Bar, Balance
from bot.strategy import Strategy, Exchange, Subscriber, ExchangeEnum
from bot.exchange.binance import BinanceUMSubscriber
from bot.exchange.okx import OkxSubscriber
from bot.executor import TradeExecutor


logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
                    level=logging.INFO)

logging.getLogger('okx.websocket.WsClientProtocol').setLevel(logging.ERROR)

__all__ = ['TradeBotConf',
           'Messager',
           'Strategy',
           'Exchange',
           'Subscriber',
           'ExchangeEnum',
           'BinanceUMSubscriber',
           'OkxSubscriber',
           'TradeExecutor',
           'Order',
           'Position',
           'Tick',
           'Bar',
           'Balance']

