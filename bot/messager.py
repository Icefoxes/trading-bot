from datetime import datetime
import logging
import requests
from bot import TradeBotConf


class Messager:
    def __init__(self, conf: TradeBotConf) -> None:
        self.prefix = conf.prefix
        self.start, self.end = conf.period.split('-')
        self.url = f'https://oapi.dingtalk.com/robot/send?access_token={conf.token}'
        self.session = requests.session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        self.last_notify = datetime.now()

    def notify(self, text) -> bool:
        data = {
            'msgtype': 'text',
            'text': {
                'content': f'{self.prefix} {text}'
            }
        }
        if datetime.now().hour > int(self.start) and datetime.now().hour < int(self.end):
            response = self.session.post(self.url, json=data)
            return 'errmsg' in response.json() and response.json()['errmsg'] == 'ok'
        else:
            logging.info('message = {text} not sent')

    def notify_with_interval(self, text) -> bool:
        if (datetime.now() - self.last_notify).seconds >= 5 * 60:
            self.last_notify = datetime.now()
            self.notify(text)
