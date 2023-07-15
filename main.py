from bot.strategies import NotificationStrategy
from bot import Messager, TradeExecutor, TradeBotConf
import asyncio
import logging

if __name__ == '__main__':
    logging.info('[1] init conf')
    conf = TradeBotConf.load()

    logging.info('[2] init messager')
    messager = Messager(conf)

    logging.info('[3] init messager')
    stragety = NotificationStrategy(messager)
  
    logging.info('[4] init executor')
    executor = TradeExecutor(stragety, backtesting=False)
    
    asyncio.run(executor.execute())
