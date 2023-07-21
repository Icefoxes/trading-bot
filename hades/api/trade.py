from fastapi import APIRouter
from hades.core import exchange

trade_router = APIRouter()

@trade_router.get('')
async def get_history_trades(symbol: str):
    return [record._asdict() for record in exchange.get_trades(symbol)]
