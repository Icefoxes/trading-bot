from configparser import ConfigParser
from os import path

class TradeBotConf:
    def __init__(self, conf: ConfigParser) -> None:
        self.apiKey         = conf['exchange']['apiKey']
        self.secretKey      = conf['exchange']['secretKey']
        self.passphrase     = conf['exchange']['passphrase']
        self.ws_private     = conf['exchange']['ws_private']
        self.ws_public      = conf['exchange']['ws_public']
        self.ws_business    = conf['exchange']['ws_business']
        self.domain         = conf['exchange']['domain']
        self.useServerTime  = conf.getboolean('exchange', 'useServerTime')
        self.token          = conf['notification']['token']
        self.prefix         = conf['notification']['prefix']
        self.period         = conf['notification']['period']
    
    @staticmethod
    def load():
        parser = ConfigParser()
        parser.read(path.join(path.dirname(path.dirname(__file__)), 'app.conf'), encoding='UTF-8')
        return TradeBotConf(parser)
    
    def __str__(self) -> str:
        return self.apiKey