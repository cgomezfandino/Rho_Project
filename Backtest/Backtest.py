__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts
import Functions.Indicators as ind
import Functions.Candles_Patterns as candle
import connection.Conn_Oanda as conn




cnx = conn.Initialize('EUR_USD', start = '2015-01-01', end = '2017-01-01', timeFrame = 'H4')
df = cnx.get_data()

SMA=30

df['SMA_%i' %SMA]= ind.sma(df, periods=SMA)

print(df)

