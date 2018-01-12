__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts


def candles_engulfing_pattern(df):

    df['Envolvente'] = np.nan
    df['Envolvente'] = np.where(((df.incDec.shift(1) == -1) & (df.OpenAsk <= df.CloseAsk.shift(1)) & (df.CloseAsk > df.OpenAsk.shift(1))), 1,np.nan)
    df['Envolvente'] = np.where(((df.incDec.shift(1) == 1) & (df.OpenAsk >= df.CloseAsk.shift(1)) & (df.CloseAsk < df.OpenAsk.shift(1))), 1, df['Envolvente'])
    return df.Envolvente

def candles_bull_bear(df):

    df['incDec'] = np.where(df.CloseAsk > df.OpenAsk, 1, -1)
    return df.incDec

