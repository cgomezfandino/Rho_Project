__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts


def candles_engulfing_pattern(df):

    df_ = df.copy()
    df_['Envolvente'] = np.nan
    df_['Envolvente'] = np.where(((df.incDec.shift(1) == -1) & (df.open <= df.close.shift(1)) & (df.close > df.open.shift(1))), 1, np.nan)
    df_['Envolvente'] = np.where(((df.incDec.shift(1) == 1) & (df.open >= df.close.shift(1)) & (df.close < df.open.shift(1))), 1, df_['Envolvente'])
    return df_.Envolvente

def candles_bull_bear(df):

    df_ = df.copy()
    df_['incDec'] = np.where(df.close > df.open, 1, -1)
    return df_.incDec

