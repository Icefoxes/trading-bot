from collections import namedtuple

Tick = namedtuple('Tick', ['symbol', 'price', 'timestmap'])

Bar = namedtuple('Bar', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])

Order = namedtuple('Orders', ['orderId', 'orderType', 'symbol', 
                              'instrumentType', 'price', 
                                'status', 'side', 'quantity', 'timestamp'])

Position = namedtuple('Position', ['symbol', 'instrumentType', 
                                   'side', 'quantity', 'unrealized_profit', 
                                   'unrealized_profit_ratio', 'mode', 'price', 'timestamp'])

Balance = namedtuple('Balance',['asset', 'availableBalance'])

Trade = namedtuple('Trade', ['symbol', 
                             'id', 
                             'orderId', 
                             'side', 
                             'price', 
                             'quantity',
                             'realizedPnl',
                             'marginAsset', 
                             'quoteQty', 
                             'commission', 
                             'commissionToUSDT', 
                             'commissionAsset', 
                             'timestamp',
                             'maker'])