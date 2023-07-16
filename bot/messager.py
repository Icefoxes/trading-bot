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
        self.last_notify = None

    def notify(self, text) -> bool:
        data = {
            'msgtype': 'text',
            'text': {
                'content': f'{self.prefix} {text}'
            }
        }
        now = datetime.utcnow()
        if now.hour >= int(self.start) and now.hour < int(self.end):
            response = self.session.post(self.url, json=data)
            return 'errmsg' in response.json() and response.json()['errmsg'] == 'ok'
        else:
            logging.info('message = {text} not sent')

    def notify_with_interval(self, text, minute: int = 5) -> bool:
        now = datetime.utcnow()
        if not self.last_notify or (now - self.last_notify).seconds >= minute * 60:
            self.last_notify = now
            self.notify(text)
