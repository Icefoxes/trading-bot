from bot.exchange.binance import BinanceUMExchangeClient
from bot import TradeBotConf

exchange = BinanceUMExchangeClient(TradeBotConf.load())