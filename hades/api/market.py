from fastapi import APIRouter
from hades.core import exchange

market_router = APIRouter()

@market_router.get('')
async def get_kline(symbol: str, interval: str, limit: int=100):
    return [record._asdict() for record in exchange.get_candlesticks(symbol=symbol, bar=interval, limit=limit)]
