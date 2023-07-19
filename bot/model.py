from collections import namedtuple

Tick = namedtuple('Tick', ['instrument', 'price', 'timestmap'])

Bar = namedtuple('Bar', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])

Order = namedtuple('Orders', ['orderId', 'orderType', 'instrument', 
                              'instrumentType', 'price', 'mode',
                                'status', 'side', 'lever', 'qty', 'timestamp'])

Position = namedtuple('Position', ['positionId','instrument', 'instrumentType', 
                                   'side', 'quantity', 'unrealized_profit', 
                                   'pnl_ratio', 'mode', 'price', 'last','timestamp'])

Balance = namedtuple('Balance',['availableBalance'])
