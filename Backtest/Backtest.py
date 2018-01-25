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
import talib




if __name__ == '__main__':
    # Conexion con base de datos
    cnx = conn.Initialize('EUR_USD', start = '2015-01-01', end = '2017-01-01', timeFrame = 'H4')
    df = cnx.get_data()

    # Inicializacion de Datos:

    amount = 1000 #Capital Inicial
    SMA= 200 # Moving Average
    EMA = 200 # Exponential Moving Avg
    momentum = 20
    r = 0.0255 #Risk Free Rate
    roll = 100 #Rolling to calulate the kelly Criterion
    transactionCost = 0.000

    df['SMA_%i' %SMA] = talib.SMA(np.array(df.close), SMA)


    # df['EMA_%i' %EMA] = ind.sma(df, periods=EMA)

    # Identificacion de velas alcistas y bajistas:
    df['incDec'] = candle.candles_bull_bear(df)

    # Indentificacion de velas Envolventes:

    # https: // github.com / mrjbq7 / ta - lib / blob / master / docs / func_groups / pattern_recognition.md

    # df['engulf'] = candle.candles_engulfing_pattern(df)

    df['engulfing'] = talib.CDLENGULFING(np.array(df.open), np.array(df.high),
                                         np.array(df.low), np.array(df.close))

    df['engulfing'] = np.abs(df['engulfing'])
    df['engulfing'] = np.where(df['engulfing']==100, 1, np.nan)

    df['hammer'] = talib.CDLHAMMER(np.array(df.open), np.array(df.high),
                         np.array(df.low), np.array(df.close))

    df['hammer'] = np.where(df['hammer'] == 100, 1, np.nan)


    # comprobacion
    # df.to_csv(r'../Oanda/prueba.csv', sep=';')

    # Calculo de los retornos:
    df['returns'] = np.log(df['close']/df['close'].shift(1))

    # Calculo de apalancamianto: Kelly Criterion
    df['KellyCriterion'] = ind.KellyCriterion(df,roll = roll,r = r,halfKC = True)

    # Calcilo de Momentum:

    df['cstrategy_p'],df['cstrategy_c'], df['mmt_position']  = ind.momentum(df, momentum=momentum, amount = amount, transactionCost = transactionCost)



    # Plotea
    bkp.bokeh_Plotting(df, periodos=SMA)

    print(df)

