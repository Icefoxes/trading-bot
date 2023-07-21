from starlette.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

from bot.exchange.binance import BinanceUMExchangeClient
from bot import TradeBotConf

exchange = BinanceUMExchangeClient(TradeBotConf.load())


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code == 404:
                response = await super().get_response('.', scope)
        return response
