from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bot.exchange.binance import BinanceUMExchangeClient
from bot import TradeBotConf

exchange = BinanceUMExchangeClient(TradeBotConf.load())

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

@app.get("/api/v1/klines")
async def get_kline(symbol: str, interval: str, limit: int=100):
    return [record._asdict() for record in exchange.get_candlesticks(symbol=symbol, bar=interval, limit=limit)]

@app.get("/api/v1/positions")
async def get_positions():
    return [record._asdict() for record in exchange.get_positions()]

@app.get("/api/v1/orders")
async def get_orders():
    return [record._asdict() for record in exchange.get_orders()]

app.mount("/", StaticFiles(directory="hades-ui/build", html=True), name="build")

print(app.routes)
