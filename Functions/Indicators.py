__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts


def KellyCriterion(df, roll = 100, r = 0.0225, halfKC = True):

    df_ = df.copy()

    if halfKC is True:
        df_['meanRoll'] = df_['returns'].rolling(roll).mean() * 6 * 252
        df_['stdRoll'] = df_['returns'].rolling(roll).std() * 6 * 252 ** 0.5
        df_['KC'] = np.where( ((df_['meanRoll'] - r) / df_['stdRoll']**2)/2 < 1, 1, ((df_['meanRoll'] - r) / df_['stdRoll']**2)/2 )
        df_['KC'].fillna(1,inplace =True)
    else:
        df_['meanRoll'] = df_['returns'].rolling(roll).mean() * 6 * 252
        df_['stdRoll'] = df_['returns'].rolling(roll).std() * 6 * 252 ** 0.5
        df_['KC'] = np.where( ((df_['meanRoll'] - r) / df_['stdRoll']**2) < 1, 1, ((df_['meanRoll'] - r) / df_['stdRoll']**2) )
        df_['KC'].fillna(1,inplace =True)


    return df_['KC']



def sma(df, price = 'CloseAsk', periods = 50):

    """

    :param df:
    :param price: OpenAsk, HighAsk, LowAsk, CloseAsk
    :param periods:
    :return: SMA
    """

    SMA = df[price].rolling(periods).mean()

    return SMA

def momentum(df, momentum = 20, amount = 10000, transactionCost = 0.000):

    df_ = df.copy()

    # Buy and Hold
    # In Cash
    df_['creturns_c'] = amount * df_['returns'].cumsum().apply(np.exp)
    # In Percentage
    df_['creturns_p'] = df_['returns'].cumsum().apply(np.exp)


    ## Applying the Strategy

    # Getting the strategy
    df_['position'] = np.sign(df_['returns'].rolling(momentum).mean())
    df_['strategy'] = df_['position'].shift(1) * df_['returns']

    # Applying the laverage
    df_['lstrategy'] = df_['strategy'] * df_['KellyCriterion']

    ## determinate when a trade takes places (long or short)
    trades = df_['position'].diff().fillna(0) != 0

    ## subtracting transaction cost from return when trade takes place
    df_['lstrategy'][trades] -= transactionCost

    ## Returns in Cash
    df_['cstrategy_c'] = amount * df_['lstrategy'].cumsum().apply(np.exp)

    ## Returns in percentage
    df_['cstrategy_p'] = df_['lstrategy'].cumsum().apply(np.exp)

    # ## Max Cummulative returns in cash
    # df_['cmstrategy_c'] = df_['cstrategy_c'].cummax()
    #
    # ## Max Cummulative returns in percentage
    # df_['cmstrategy_p'] = df_['cstrategy_p'].cummax()
    #
    # ## Max Drawdown un Cash
    # df_['ddstrategy_c'] = df_['cmstrategy_c'] - df_['cstrategy_c']
    #
    # ## Max Drawdown in Percentage
    # df_['ddstrategy_p'] = df_['cmstrategy_p'] - df_['cstrategy_p']

    return df_['cstrategy_p'], df_['cstrategy_c'], df_['position']








#
# cols = ['CloseAsk','HighAsk','LowAsk','OpenAsk','volume']
# df = pd.read_table(r'D:\Rho_Project\Oanda\EUR_USD_H4_15-17.csv',sep=',')
# df.index = df.time
# df = df[cols]
# df.rename(columns={"CloseAsk": "CloseAsk_EUR_USD"},inplace=True)
#
# df2 = pd.read_table(r'D:\Rho_Project\Oanda\GBP_USD_H4_15-17.csv',sep=',')
# df2.index = df2.time
# df2 = df2[cols]
# df2.rename(columns={"CloseAsk": "CloseAsk_GBP_USD"},inplace=True)
# df3 = pd.concat([df['CloseAsk_EUR_USD'], df2['CloseAsk_GBP_USD']], axis=1, join='inner')
# df3.index= df.index
#
# X = df['CloseAsk_EUR_USD'][1:200]
# Y = df2['CloseAsk_GBP_USD'][1:200]
#
# X=X.reshape(len(X),1)
# Y=Y.reshape(len(Y),1)
#
# model = linear_model.LinearRegression()
#
# model_fit = model.fit(X=X, y=Y)
#
# mr = Y - model_fit.coef_ * X
#
# lrm = (model_fit.coef_ * X) + model_fit.intercept_
#
# # plt.plot(X,Y,'ro',X,lrm) Plot with regression
#
# # df3.plot(figsize=(8,7), subplots=False)
# # plt.show()
#
#
# print(df3)
