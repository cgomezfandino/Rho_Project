__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts
import Functions.Indicators as ind
import Functions.Candles_Patterns as candle




if __name__ == '__main__':
    df = pd.read_table(r'D:\Rho_Project\Oanda\EUR_USD_H4_15-17.csv', sep=',')
    candle.candles_bull_bear(df)
    candle.candles_engulfing_pattern(df)
    ind.sma(df, price= 'CloseAsk', periods=50)
    print(df)