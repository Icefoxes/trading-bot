from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
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


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code == 404:
                response = await super().get_response('.', scope)
        return response

app.mount("/web/", SPAStaticFiles(directory="hades-ui/build", html=True), name="web")

print(app.routes)
