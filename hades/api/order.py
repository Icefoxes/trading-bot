from fastapi import APIRouter
from hades.core import exchange

order_router = APIRouter()

@order_router.get('')
async def get_orders():
    return [record._asdict() for record in exchange.get_orders()]
