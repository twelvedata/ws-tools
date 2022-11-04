import datetime
import logging
import time
import typing

from twelvedata import TDClient


class SubscriptionMonitoring:

    def __init__(self, apikey: str, symbols: typing.List[str]):
        self.symbols = symbols
        self.apikey = apikey
        # Keys are symbols, values are time
        self.last_actions = {}
        self.stat_intervals = {
            '10 sec': datetime.timedelta(seconds=10),
            '20 sec': datetime.timedelta(seconds=20),
            '30 sec': datetime.timedelta(seconds=30),
            '1 min': datetime.timedelta(seconds=60),
            '2 min': datetime.timedelta(seconds=120),
            '5 min': datetime.timedelta(seconds=300),
            '30 min': datetime.timedelta(seconds=1800),
        }

    def get_stat(self) -> typing.List[dict]:
        now = datetime.datetime.now()
        stat = []
        for k, v in self.stat_intervals.items():
            item = {
                'interval': k,
                'fresh': 0,
            }
            for symbol, symbol_at in self.last_actions.items():
                if now - symbol_at <= v:
                    item['fresh'] += 1
            stat.append(item)
        return stat

    def on_event(self, e):
        now = datetime.datetime.now()
        if e['event'] == 'price':
            self.last_actions[e['symbol']] = now

    def run(self):
        td = TDClient(apikey=self.apikey)
        ws = td.websocket(
            symbols=','.join(self.symbols),
            on_event=self.on_event,
        )
        ws.connect()

        while True:
            time.sleep(10)

            stat = self.get_stat()
            logging.info('-----')
            for item in stat:
                logging.info('Interval {0}. {1}/{2}. {3} %.'.format(
                    item['interval'],
                    item['fresh'],
                    len(self.symbols),
                    100 * item['fresh'] / (len(self.symbols) if len(self.symbols) > 0 else 1),
                ))

            ws.heartbeat()
