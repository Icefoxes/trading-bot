from configparser import ConfigParser
from os import path

class TradeBotConf:
    def __init__(self, conf: ConfigParser) -> None:
        self.okx                   = {}
        self.okx['apiKey']         = conf['okx']['apiKey']
        self.okx['secretKey']      = conf['okx']['secretKey']
        self.okx['passphrase']     = conf['okx']['passphrase']
        self.okx['ws_private']     = conf['okx']['ws_private']
        self.okx['ws_public']      = conf['okx']['ws_public']
        self.okx['ws_business']    = conf['okx']['ws_business']
        self.okx['domain']         = conf['okx']['domain']
        self.okx['useServerTime']  = conf.getboolean('okx', 'useServerTime')
        self.binance               = {}
        self.binance['apiKey']     = conf['binance']['apiKey']
        self.binance['secretKey']  = conf['binance']['secretKey']
        self.token                 = conf['notification']['token']
        self.prefix                = conf['notification']['prefix']
        self.period                = conf['notification']['period']
    
    @staticmethod
    def load():
        parser = ConfigParser()
        parser.read(path.join(path.dirname(path.dirname(__file__)), 'app.conf'), encoding='UTF-8')
        return TradeBotConf(parser)
