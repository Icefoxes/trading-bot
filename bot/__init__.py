import logging

from bot.config import TradeBotConf
from bot.messager import Messager
from bot.model import Order, Position, Tick, Bar, Balance, to_tick, to_order, to_bar, to_position, to_balance
from bot.exchange import ExchangeClient
from bot.strategy import Strategy
from bot.subscribe import OrderSubscriber, PositionSubscriber, TickSubscriber, BarSubscriber, BalanceSubscribe
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
