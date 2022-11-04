import datetime
import logging
import time
import typing

from twelvedata import TDClient


class DelayMonitoring:

    def __init__(self, apikey: str, symbols: typing.List[str]):
        self.symbols = symbols
        self.apikey = apikey
        # Keys are symbols, values are time
        self.last_actions = {}
        self.stat_delays = {
            '5 sec': datetime.timedelta(seconds=5),
            '10 sec': datetime.timedelta(seconds=10),
            '30 sec': datetime.timedelta(seconds=30),
            '1 min': datetime.timedelta(seconds=60),
            '2 min': datetime.timedelta(seconds=120),
            '5 min': datetime.timedelta(seconds=300),
            '10 min': datetime.timedelta(seconds=600),
            '15 min': datetime.timedelta(seconds=900),
            '20 min': datetime.timedelta(seconds=1200),
            '30 min': datetime.timedelta(seconds=1800),
            '> 30 min': datetime.timedelta(seconds=60000),
        }

    def get_stat(self) -> (typing.List[dict], int):
        stat = []
        prev_delay = datetime.timedelta(seconds=0)
        for k, v in self.stat_delays.items():
            item = {
                'interval': k,
                'fresh': 0,
                'example': '',
            }
            for symbol, delay in self.last_actions.items():
                if prev_delay <= delay < v:
                    item['fresh'] += 1
                    item['example'] = symbol
            stat.append(item)
            prev_delay = v
        return stat, len(self.last_actions.items())

    def on_event(self, e):
        # {"event":"price","symbol":"AMZN","currency":"USD","exchange":"NASDAQ","type":"Common Stock","timestamp":1667563304,"price":90.39}
        if e['event'] == 'price':
            now = datetime.datetime.utcnow()
            self.last_actions[e['symbol']] = now - datetime.datetime.utcfromtimestamp(e['timestamp'])

    def run(self):
        td = TDClient(apikey=self.apikey)
        ws = td.websocket(
            symbols=','.join(self.symbols),
            on_event=self.on_event,
        )
        ws.connect()

        while True:
            time.sleep(10)

            stat, total = self.get_stat()
            self.last_actions = {}
            logging.info('-----')
            for item in stat:
                logging.info('Delay {0}. {1}/{2}. {3} %. {4}'.format(
                    item['interval'],
                    item['fresh'],
                    len(self.symbols),
                    round(100 * item['fresh'] / (total if total > 0 else 1), 2),
                    item['example']
                ))

            ws.heartbeat()
