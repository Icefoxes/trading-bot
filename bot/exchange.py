
from bot import TradeBotConf
import okx.Trade as Trade
import okx.Account as Account


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

    def get_positions(self):
        return self.accountApi.get_positions()

    def get_balance(self):
        return self.accountApi.get_account_balance()

    def get_orders(self):
        return self.tradeApi.get_order_list()
    
    def place_buy_order(self, instrumentId: str, size: float, price: float):
        return self.tradeApi.place_order(instId=instrumentId, tdMode='isolated', side='buy', sz=str(size), px=str(price), ordType='post_only')
    
    def place_sell_order(self, instrumentId: str, size: float, price: float):
        return self.tradeApi.place_order(instId=instrumentId, tdMode='isolated', side='sell', sz=str(size), px=str(price), ordType='post_only')
    
    def cancel_order(self, orderId: str, instrumentId: str):
        return self.tradeApi.cancel_order(instId=instrumentId, ordId=orderId)
    
    def close_position(self, instrumentId: str):
        return self.tradeApi.close_positions(instId=instrumentId)