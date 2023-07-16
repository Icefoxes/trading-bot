
from bot import TradeBotConf, Bar, to_bar, Position, to_position, Order, to_order
from typing import List
import okx.Trade as Trade
import okx.Account as Account
import okx.MarketData as Market


class ExchangeClient:
    def __init__(self,  conf: TradeBotConf) -> None:
        self.conf = {
            'api_key': conf.apiKey,
            'api_secret_key': conf.secretKey,
            'domain': conf.domain,
            'passphrase': conf.passphrase,
            'flag': '0'
        }
        self.tradeApi = Trade.TradeAPI(**self.conf)
        self.accountApi = Account.AccountAPI(** self.conf)
        self.marketApi = Market.MarketAPI(**self.conf)
    # Account Info
    def get_positions(self) -> List[Position]:
        response = self.accountApi.get_positions()
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_position(response['data']) 
        return []

    def get_balance(self):
        return self.accountApi.get_account_balance()
    # Trade Info
    def get_orders(self) -> List[Order]:
        response = self.tradeApi.get_order_list()
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_order(response['data']) 
        return []
    
    def place_buy_order(self, instrumentId: str, size: float, price: float):
        return self.tradeApi.place_order(instId=instrumentId, tdMode='isolated', side='buy', sz=str(size), px=str(price), ordType='post_only')
    
    def place_sell_order(self, instrumentId: str, size: float, price: float):
        return self.tradeApi.place_order(instId=instrumentId, tdMode='isolated', side='sell', sz=str(size), px=str(price), ordType='post_only')
    
    def cancel_order(self, orderId: str, instrumentId: str):
        return self.tradeApi.cancel_order(instId=instrumentId, ordId=orderId)
    
    def close_position(self, instrumentId: str):
        return self.tradeApi.close_positions(instId=instrumentId, mgnMode='isolated')

    # get latest 100 bar
    def get_candlesticks(self, instrumentId: str, bar: str = '1m', limit: int = 100) -> List[Bar]:
        response = self.marketApi.get_candlesticks(instId=instrumentId, bar=bar, limit=str(limit))
        if response.get('code') == '0' and response.get('data') and len(response['data']) > 0:
            return to_bar(response['data']) 
        return []
    