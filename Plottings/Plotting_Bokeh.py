from math import pi
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
# https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html

df = pd.read_csv(r'..\Oanda\EUR_USD_H4_15-17.csv', sep=',')
cols = ['time', 'OpenAsk', 'CloseAsk', 'HighAsk', 'LowAsk', 'volume']
df = df[cols]
df['percent'] = np.log(df.CloseAsk / df.CloseAsk.shift(1))

df['SMA'] = df.CloseAsk.rolling(10).mean()

df.time = pd.to_datetime(df.time)

df = df[:200]

inc = df.CloseAsk > df.OpenAsk
dec = df.OpenAsk > df.CloseAsk
w = 0.5

source = ColumnDataSource(df)



# hover = HoverTool(tooltips=[
#     ("date", "@time"),
#     ("open", "@OpenAsk"),
#     ("close", "@CloseAsk"),
#     ("percent", "@percent"),
# ])

TOOLS = ["pan,wheel_zoom,box_zoom,reset,save"]

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "EUR_USD Candlestick")

# map dataframe indices to date strings and use as label overrides
p.xaxis.major_label_overrides = {i: date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(df["time"]))}
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.5

p.segment(df.index, df.HighAsk, df.index, df.LowAsk, color="black")
p.vbar(df.index[inc], w, df.OpenAsk[inc], df.CloseAsk[inc], color="white", line_color="black")
p.vbar(df.index[dec], w, df.OpenAsk[dec], df.CloseAsk[dec], color="black", line_color="black")

p.line(df.index, df.SMA)

output_file("candlestick.html", title="candlestick.py example")

show(p)  # open a browser