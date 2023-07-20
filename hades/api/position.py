from fastapi import APIRouter
from hades.core import exchange

position_router = APIRouter()

@position_router.get('')
async def get_positions():
    return [record._asdict() for record in exchange.get_positions()]
