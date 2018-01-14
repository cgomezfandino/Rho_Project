from math import pi
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
import time
import Functions.Indicators as ind
import Functions.Candles_Patterns as candle
# import SandBox.Pruebas as sb

# https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html


def bokeh_Plotting(df, periodos = 10, positions = None):

    '''

    :param df: DataFrame
    :param periodos: Calculate MA to Plot
    :param positions: position_20, position_40 ... position_n
    :return: Bokeh's Plots
    '''

    if positions is None:
        print('No results to plot yet. Run a strategy.')

    for position in positions:

        start = time.time()
        cols = ['OpenAsk', 'CloseAsk', 'HighAsk', 'LowAsk', 'volume', position]
        df_plot = df[cols]
        # df_plot['percent'] = np.log(df_plot.CloseAsk / df_plot.CloseAsk.shift(1))

        df_plot[position] = np.where(df_plot[position] == 0, np.nan, df_plot[position])

        df_plot[position] = np.where(df_plot[position] == -1, 1, df_plot[position])

        df_plot.index = range(0,len(df_plot))

        # Cálculo de Media Movil
        periods_ = periodos
        df_plot['SMA_%i' %periods_] = ind.sma(df_plot, periods = periods_)

        df_plot['time'] = df_plot.index.values

        df_plot.time = pd.to_datetime(df_plot.time)

        df_plot = df_plot[:200]

        inc = df_plot.CloseAsk > df_plot.OpenAsk
        dec = df_plot.OpenAsk > df_plot.CloseAsk
        w = 0.5

        # Bull or Bear Candle
        df_plot['incDec'] = candle.candles_bull_bear(df_plot)
        # Patron Envolvente
        df_plot['engulf'] = candle.candles_engulfing_pattern(df_plot)

        source = ColumnDataSource(df_plot)


        # hover = HoverTool(tooltips=[
        #     ("date", "@time"),
        #     ("open", "@OpenAsk"),
        #     ("close", "@CloseAsk"),
        #     ("percent", "@percent"),
        # ])

        TOOLS = ["pan,wheel_zoom,box_zoom,reset,save"]

        p = figure(x_axis_type = "datetime", tools = TOOLS, plot_width = 1000, title = "EUR_USD Candlestick - Momentum %s" %position)


        # map dataframe indices to date strings and use as label overrides
        p.xaxis.major_label_overrides = {i: date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(df_plot["time"]))}
        p.xaxis.major_label_orientation = pi/4
        p.grid.grid_line_alpha = 0.5

        p.segment(df_plot.index, df_plot.HighAsk, df_plot.index, df_plot.LowAsk, color="black")

        # Plotting Candles
        p.vbar(df_plot.index[inc], w, df_plot.OpenAsk[inc], df_plot.CloseAsk[inc], color="white", line_color="black")
        p.vbar(df_plot.index[dec], w, df_plot.OpenAsk[dec], df_plot.CloseAsk[dec], color="black", line_color="black")

        # Plotting SMA
        p.line(df_plot.index, df_plot['SMA_%i' %periods_])

        # Plotting Engulfing Pattern
        p.circle(df_plot.index, df_plot.LowAsk * df_plot.engulf)

        p.triangle(df_plot.index, df_plot.HighAsk * df_plot[position], color="firebrick")
        output_file("candlestick.html", title="candlestick.py example")
        show(p)  # open a browser
        print("%3.2f Seconds" %(time.time() - start))

if __name__ == '__main__':

    df = pd.read_csv(r'..\Oanda\EUR_USD_H4_15-17.csv', sep=',')
    bokeh_Plotting(df, positions=10)

