from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hades.api import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router, prefix='/api/v1/klines')
app.include_router(position_router, prefix='/api/v1/positions')
app.include_router(order_router, prefix='/api/v1/orders')
app.include_router(balance_router, prefix='/api/v1/balances')
app.include_router(trade_router, prefix='/api/v1/trades')

print(app.routes)
