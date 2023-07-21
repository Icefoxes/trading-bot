from configparser import ConfigParser
from os import path
import os

BINANCE_API_KEY      = 'BINANCE_API_KEY'
BINANCE_SECRET_KEY   = 'BINANCE_SECRET_KEY'

NOTIFICATION_TOKEN  = 'NOTIFICATION_TOKEN'
NOTIFICATION_PREFIX = 'NOTIFICATION_PREFIX'
NOTIFICATION_PERIOD = 'NOTIFICATION_PERIOD'

class TradeBotConf:
    def __init__(self, conf: ConfigParser = None) -> None:
        if not conf:
            self.binance               = {}
            self.binance['apiKey']     = os.environ.get(BINANCE_API_KEY)
            self.binance['secretKey']  = os.environ.get(BINANCE_SECRET_KEY)
            self.token                 = os.environ.get(NOTIFICATION_TOKEN)
            self.prefix                = os.environ.get(NOTIFICATION_PREFIX)
            self.period                = os.environ.get(NOTIFICATION_PERIOD)
        else:
            if conf.has_section('okx'):
                self.okx                   = {}
                self.okx['apiKey']         = conf['okx']['apiKey']
                self.okx['secretKey']      = conf['okx']['secretKey']
                self.okx['passphrase']     = conf['okx']['passphrase']
                self.okx['ws_private']     = conf['okx']['ws_private']
                self.okx['ws_public']      = conf['okx']['ws_public']
                self.okx['ws_business']    = conf['okx']['ws_business']
                self.okx['domain']         = conf['okx']['domain']
                self.okx['useServerTime']  = conf.getboolean('okx', 'useServerTime')
            if conf.has_section('binance'):
                self.binance               = {}
                self.binance['apiKey']     = conf['binance']['apiKey']
                self.binance['secretKey']  = conf['binance']['secretKey']
            if conf.has_section('notification'):
                self.token                 = conf['notification']['token']
                self.prefix                = conf['notification']['prefix']
                self.period                = conf['notification']['period']
        
    
    @staticmethod
    def load():
        parser = ConfigParser()
        ROOT_DIR = os.path.abspath(os.curdir)
        conf_file = path.join(ROOT_DIR, 'app.conf')
        if path.exists(conf_file):
            parser.read(conf_file, encoding='UTF-8')
            return TradeBotConf(parser)
        else:
            return TradeBotConf()
