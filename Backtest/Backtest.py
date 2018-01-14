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
import Plottings.Plotting_Bokeh as bkp




if __name__ == '__main__':
    # Conexion con base de datos
    cnx = conn.Initialize('EUR_USD', start = '2015-01-01', end = '2017-01-01', timeFrame = 'H4')
    df = cnx.get_data()

    # Inicializacion de Datos:

    amount = 1000 #Capital Inicial
    SMA= 200 # Moving Average
    momentum = 20
    r = 0.0255 #Risk Free Rate
    roll = 100 #Rolling to calulate the kelly Criterion
    transactionCost = 0.000

    df['SMA_%i' %SMA]= ind.sma(df, periods=SMA)

    # Identificacion de velas alcistas y bajistas:
    df['incDec'] = candle.candles_bull_bear(df)

    # Indentificacion de velas Envolventes:
    df['engulf'] = candle.candles_engulfing_pattern(df)

    # Calculo de los retornos:
    df['returns'] = np.log(df['CloseAsk']/df['CloseAsk'].shift(1))

    # Calculo de apalancamianto: Kelly Criterion
    df['KellyCriterion'] = ind.KellyCriterion(df,roll = roll,r = r,halfKC = True)

    # Calcilo de Momentum:

    df['cstrategy_p'],df['cstrategy_c'], df['mmt_position']  = ind.momentum(df, momentum=momentum, amount = amount, transactionCost = transactionCost)



    # Plotea
    bkp.bokeh_Plotting(df, 10)

    print(df)

