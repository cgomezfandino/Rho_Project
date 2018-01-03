import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model


df = pd.read_csv(r'..\Oanda\EUR_USD_H4_15-17.csv', sep=',')

lags = 2

m = np.zeros((lags + 1, len(df) - lags))

for i in range(lags + 1):
    if i == lags:
        m[i] = df.CloseAsk.iloc[i:]
    else:
        m[i] = df.CloseAsk.iloc[i:i - lags]

lm = linear_model.LinearRegression()
reg = lm.fit(m[:lags].T, m[lags])
# LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1,normalize=False)

pred = lm.predict(m[:lags].T)
# reg
df['pred'] = 0.0
df['pred'].iloc[lags:] = pred

df[['CloseAsk', 'pred']].ix[lags:].plot(figsize=(10, 6))
plt.show()

df['strategy'] = df['pred'] * df['returns']


df[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
plt.show()
df