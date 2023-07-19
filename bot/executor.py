from bot import Strategy, BinanceUMSubscriber, OkxSubscriber, Subscriber, ExchangeEnum


class TradeExecutor():
    def __init__(self, strategy: Strategy, backtesting: bool, exchange:ExchangeEnum=ExchangeEnum.Binance) -> None:
        self.backtesting = backtesting
        self.strategy = strategy
        self.exchange = exchange
        self.subscriber = self.__get_subscriber(self.exchange)

    async def execute(self):
        await self.subscriber.run()

    def __get_subscriber(self, exchange:ExchangeEnum) -> Subscriber:
        if exchange == ExchangeEnum.Binance:
            return BinanceUMSubscriber(self.strategy)
        elif exchange == ExchangeEnum.OKX:
            return OkxSubscriber(self.strategy)
        raise  ValueError('current exchange does not support')
    
    def stop(self):
        self.subscriber.stop()
        
