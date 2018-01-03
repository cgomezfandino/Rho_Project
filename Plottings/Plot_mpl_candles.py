import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.finance as mpf
import datetime as dt
from matplotlib import dates as mdates


def graph_candles(symbol):

    fig, ax = plt.subplots(figsize=(8,7))
    fig.subplots_adjust(bottom=0.2)
    symbol['time'] = mdates.date2num(symbol['time'].astype(dt.date))
    mpf._candlestick(ax, symbol.values, width=0.6, colorup= 'b', colordown='r')
    plt.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv(r'..\Oanda\EUR_USD_H4_15-17.csv', sep=',')
    cols = ['time','OpenAsk','CloseAsk','HighAsk','LowAsk','volume']
    df = df[cols]
    df.time = pd.to_datetime(df.time)
    df = df[:100]
    graph_candles(df)
    df


