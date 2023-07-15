import logging

from bot.config import TradeBotConf
from bot.messager import Messager
from bot.strategy import Strategy, Order, Position, Tick, Bar, to_tick, to_order, to_bar, to_position
from bot.exchange import ExchangeClient
from bot.subscribe import OrderSubscriber, PositionSubscriber, TickSubscriber, BarSubscriber
from bot.executor import TradeExecutor


logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
                    level=logging.INFO)

logging.getLogger('okx.websocket.WsClientProtocol').setLevel(logging.ERROR)

__all__ = ['TradeBotConf',
           'Messager',
           'ExchangeClient',
           'BarSubscriber'
           'TickSubscriber',
           'PositionSubscriber'
           'OrderSubscriber',
           'TradeExecutor',
           'Strategy',
           'Order',
           'Position',
           'Tick',
           'Bar'
           ]
