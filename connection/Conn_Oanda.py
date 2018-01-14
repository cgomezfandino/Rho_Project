__author__ = 'cgomezfandino@gmail.com'

import datetime as dt
import v20
from configparser import ConfigParser
import pandas as pd
import numpy as np


class Initialize(object):

    def __init__(self, symbol, start, end, sufix='.000000000Z', timeFrame='H4',
                 price='A'):

        self.symbol = symbol
        self.suffix = sufix
        self.timeFrame = timeFrame
        self.price = price
        self.start = dt.datetime.combine(pd.to_datetime(start), dt.time(9, 00))
        self.end = dt.datetime.combine(pd.to_datetime(end), dt.time(16, 00))
        self.fromTime = self.start.isoformat('T') + self.suffix
        self.toTime = self.end.isoformat('T') + self.suffix
        self.data = []

        config = ConfigParser()
        config.read(r'../connection/pyalgo.cfg')

        self.ctx = v20.Context(
            'api-fxpractice.oanda.com',
            443,
            True,
            application='sample_code',
            token=config['oanda_v20']['access_token'],
            datetime_format='RFC3339')

        # self.get_data()

    def get_data(self):

        res = self.ctx.instrument.candles(
            instrument=self.symbol,
            fromTime=self.fromTime,
            toTime=self.toTime,
            granularity=self.timeFrame,
            price=self.price)

        raw = res.get('candles')

        raw = [cs.dict() for cs in raw]

        for cs in raw:
            cs.update(cs['ask'])
            del cs['ask']

        data = pd.DataFrame(raw)

        data['time'] = pd.to_datetime(data['time'], unit='ns')

        data = data.set_index('time')

        data.index = pd.DatetimeIndex(data.index)

        # print data.info()

        cols = ['c', 'l', 'h', 'o']

        data[cols] = data[cols].astype('float64')

        data.rename(columns={'c': 'CloseAsk', 'l': 'LowAsk',
                             'h': 'HighAsk', 'o': 'OpenAsk'}, inplace=True)

        self.data = data

        return self.data

