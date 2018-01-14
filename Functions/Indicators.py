__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts



def sma(df, price = 'CloseAsk', periods = 50):

    """

    :param df:
    :param price: OpenAsk, HighAsk, LowAsk, CloseAsk
    :param periods:
    :return: SMA
    """

    SMA = df[price].rolling(periods).mean()

    return SMA








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
