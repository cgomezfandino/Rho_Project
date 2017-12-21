import numpy as np
import pandas as pd
import pandas.io.data as web

df = web.DataReader('GOOG', data_source='google', start='01-01-2010', end= '31-12-2016')

# print df.tail()

df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['sigma'] = pd.rolling_std(df['returns'], window=100) * np.sqrt(252)

df[['returns','sigma']].plot(subplots=True, color='blue', figsize=(8,6))

# print(df.head(10))