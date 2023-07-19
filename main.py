import signal
from bot.strategies import NotificationStrategy
from bot import Messager, TradeExecutor, TradeBotConf, ExchangeEnum
import asyncio
import logging
import platform


async def shutdown(sig: signal.Signals) -> None:
    tasks = []
    for task in asyncio.all_tasks(loop):
        if task is not asyncio.current_task(loop):
            task.cancel()
            tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("Finished awaiting cancelled tasks, results: {0}".format(results))
    loop.stop()

if __name__ == '__main__':
    logging.info('[1] init conf')
    conf = TradeBotConf.load()

    logging.info('[2] init messager')
    messager = Messager(conf)

    logging.info('[3] init stragety')
    stragety = NotificationStrategy(messager)
  
    logging.info('[4] init executor')
    executor = TradeExecutor(stragety, backtesting=False, exchange=ExchangeEnum.Binance)

    loop = asyncio.get_event_loop()
    if platform.platform().find('Windows') == -1:
        for sig in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(sig)))
    try:
        loop.create_task(executor.execute())
        loop.run_forever()
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")