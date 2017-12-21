import datetime
import requests
from io import StringIO
from pandas.io.common import urlencode
import pandas as pd

BASE = 'http://finance.google.com/finance/historical'

def get_params(symbol, start, end):
    params = {
        'q': symbol,
        'startdate': start.strftime('%Y/%m/%d'),
        'enddate': end.strftime('%Y/%m/%d'),
        'output': "csv"
    }
    return params


def build_url(symbol, start, end):
    params = get_params(symbol, start, end)
    return BASE + '?' + urlencode(params)
