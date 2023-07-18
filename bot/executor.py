from bot import Strategy, BinanceUMSubscriber, OkxSubscriber, Subscriber


class TradeExecutor():
    def __init__(self, strategy: Strategy, backtesting: bool, exchange='binance') -> None:
        self.backtesting = backtesting
        self.strategy = strategy
        self.exchange = exchange
        self.subscriber = self.__get_subscriber(self.exchange)

    def execute(self):
        return self.subscriber.run()

    def __get_subscriber(self, exchange='binance') -> Subscriber:
        if exchange == 'binance':
            return BinanceUMSubscriber(self.strategy)
        elif exchange == 'okx':
            return OkxSubscriber(self.strategy)
    
    def stop(self):
        self.subscriber.stop()
        
