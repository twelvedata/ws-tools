#!/usr/bin/env python

import logging

import config
from monitoring.subscription import SubscriptionMonitoring


def run_app(conf):
    monitoring = SubscriptionMonitoring(
        symbols=conf.MONITORING_SYMBOLS.split(','),
        apikey=conf.APIKEY,
    )
    monitoring.run()


logging.getLogger().setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

run_app(config)
