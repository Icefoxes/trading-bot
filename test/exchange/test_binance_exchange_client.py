from bot import TradeBotConf
from bot.exchange.binance import BinanceUMExchangeClient
from os import path
import json
from unittest.mock import MagicMock


def test_blanace():
    conf = TradeBotConf.load()
    exchange = BinanceUMExchangeClient(conf)
    with open(path.join(path.dirname(__file__), 'balance.json'),  'r') as f:
        exchange.client.balance = MagicMock(return_value=json.loads(f.read()))

    response = exchange.get_balance()
    assert len(response) > 0

def test_position():
    conf = TradeBotConf.load()
    exchange = BinanceUMExchangeClient(conf)
    with open(path.join(path.dirname(__file__), 'position.json'),  'r') as f:
        exchange.client.account = MagicMock(return_value={'positions': json.loads(f.read())})

    response = exchange.get_positions()
    assert len(response) > 0

def test_klind():
    conf = TradeBotConf.load()
    exchange = BinanceUMExchangeClient(conf)
    with open(path.join(path.dirname(__file__), 'kline.json'),  'r') as f:
        exchange.client.klines = MagicMock(return_value=json.loads(f.read()))

    response = exchange.get_candlesticks(symbol='BTCUSDT', bar='1m')
    assert len(response) == 100