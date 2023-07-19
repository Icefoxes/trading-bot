from typing import List
import json
from bot import Balance, Order, BinanceUMSubscriber, Strategy

account_data = """
{
  "e": "ACCOUNT_UPDATE",
  "E": 1564745798939,
  "T": 1564745798938,
  "a": {
    "m": "ORDER",
    "B": [
      {
        "a": "USDT",
        "wb": "122624.12345678",
        "cw": "100.12345678",
        "bc": "50.12345678"
      },
      {
        "a": "BUSD",
        "wb": "1.00000000",
        "cw": "0.00000000",
        "bc": "-49.12345678"
      }
    ],
    "P": [
      {
        "s": "BTCUSDT",
        "pa": "0",
        "ep": "0.00000",
        "cr": "200",
        "up": "0",
        "mt": "isolated",
        "iw": "0.00000000",
        "ps": "BOTH"
      },
      {
        "s": "BTCUSDT",
        "pa": "20",
        "ep": "6563.66500",
        "cr": "0",
        "up": "2850.21200",
        "mt": "isolated",
        "iw": "13200.70726908",
        "ps": "LONG"
      },
      {
        "s": "BTCUSDT",
        "pa": "-10",
        "ep": "6563.86000",
        "cr": "-45.04000000",
        "up": "-1423.15600",
        "mt": "isolated",
        "iw": "6570.42511771",
        "ps": "SHORT"
      }
    ]
  }
}
"""

order_data = '''
{
  "e": "ORDER_TRADE_UPDATE",
  "E": 1568879465651,
  "T": 1568879465650,
  "o": {
    "s": "BTCUSDT",
    "c": "TEST",
    "S": "SELL",
    "o": "TRAILING_STOP_MARKET",
    "f": "GTC",
    "q": "0.001",
    "p": "0",
    "ap": "0",
    "sp": "7103.04",
    "x": "NEW",
    "X": "NEW",
    "i": 8886774,
    "l": "0",
    "z": "0",
    "L": "0",
    "N": "USDT",
    "n": "0",
    "T": 1568879465650,
    "t": 0,
    "b": "0",
    "a": "9.91",
    "m": false,
    "R": false,
    "wt": "CONTRACT_PRICE",
    "ot": "TRAILING_STOP_MARKET",
    "ps": "LONG",
    "cp": false,
    "AP": "7476.89",
    "cr": "5.0",
    "pP": false,
    "si": 0,
    "ss": 0,
    "rp": "0"
  }
}
'''

tick_data = '''
  {
    "e": "24hrMiniTicker",
    "E": 123456789,
    "s": "BNBUSDT",
    "c": "0.0025",
    "o": "0.0010",
    "h": "0.0025",
    "l": "0.0010",
    "v": "10000",
    "q": "18"
  }
'''

bar_data = '''
{
  "e": "kline",
  "E": 123456789,
  "s": "BNBUSDT",
  "k": {
    "t": 123400000,
    "T": 123460000,
    "s": "BNBUSDT",
    "i": "1m",
    "f": 100,
    "L": 200,
    "o": "0.0010",
    "c": "0.0020",
    "h": "0.0025",
    "l": "0.0015",
    "v": "1000",
    "n": 100,
    "x": false,
    "q": "1.0000",
    "V": "500",
    "Q": "0.500",
    "B": "123456"
  }
}
'''
def test_binance_subscriber():
    class TestStrategy(Strategy):
        def __init__(self) -> None:
            super().__init__('id', ['BTCUSDT'], 'SWAP', '1m')
            self.orders: List[Order] = []
      
        
        def on_order_status(self, orders: List[Order]):
            super().on_order_status(orders)
            self.orders.extend(orders)
          
        def on_balance_status(self, balance: Balance):
            super().on_balance_status(balance)


    strategy = TestStrategy()
    um = BinanceUMSubscriber(strategy)
    um.handle_message(json.loads(order_data.strip('\n').strip()))
    assert len(strategy.orders) > 0
    assert strategy.orders[0].status == 'NEW'
    um.handle_message(json.loads(account_data.strip('\n').strip()))
    assert len(strategy.balance) > 0
    assert strategy.balance[0].availableBalance == 50.12

    assert len(strategy.positions) > 0
    assert strategy.positions[0].unrealized_profit == 2850.21200
    um.handle_message(json.loads(tick_data))
    assert len(strategy.ticks) > 0
    assert strategy.ticks[0].price == 0.0025

    um.handle_message(json.loads(bar_data))
 