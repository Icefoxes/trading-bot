from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from hades.api import *


app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router, prefix='/api/v1/klines')
app.include_router(position_router, prefix='/api/v1/positions')
app.include_router(order_router, prefix='/api/v1/orders')
app.include_router(balance_router, prefix='/api/v1/balances')

app.mount("/", StaticFiles(directory="hades-ui/build", html=True), name="build")

print(app.routes)
