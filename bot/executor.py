from typing import List
import asyncio
from bot import OrderSubscriber, PositionSubscriber, TickSubscriber, Strategy, BarSubscriber, BalanceSubscribe


class TradeExecutor():
    def __init__(self, strategy: Strategy, backtesting: bool) -> None:
        self.backtesting = backtesting
        self.strategy = strategy

    async def execute(self) -> List[asyncio.Future]:
        return await asyncio.gather(BalanceSubscribe(self.strategy).run(),
                                    OrderSubscriber(self.strategy).run(),
                                    BarSubscriber(self.strategy).run(),
                                    TickSubscriber(self.strategy).run(),
                                    PositionSubscriber(self.strategy).run())
