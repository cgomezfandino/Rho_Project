__author__ = 'cgomezfandino@gmail.com'

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.tsa.stattools as ts
import Functions.Indicators as ind
import Functions.Candles_Patterns as candle
import talib
import datetime


#
# if __name__ == '__main__':
#     df = pd.read_table(r'D:\Rho_Project\Oanda\EUR_USD_H4_15-17.csv', sep=',')
#     candle.candles_bull_bear(df)
#     candle.candles_engulfing_pattern(df)
#     ind.sma(df, price= 'CloseAsk', periods=50)
#     print(df)

data = pd.read_csv(r'D:\Rho_Project\Oanda\EUR_USD_H4_15-17.csv', sep=',')

data.rename(columns={'close': 'Close', 'low': 'Low',
                   'high': 'High', 'open': 'Open', 'volume':
                    'Volume'}, inplace=True)

data['pr_chg'] = data['Close'].shift(1)-data['Close'].shift(6)

data['std_100day'] = pd.rolling_std(data['pr_chg'],window=100)

data['5d_avg_vol'] = pd.rolling_mean(data['Volume'].shift(1),window=5)

data['past 5d_avg_vol'] = data['5d_avg_vol'].shift(5)

data['signal']=0

data.loc[((data['pr_chg'].abs() > data['std_100day']) & (data['5d_avg_vol']<data['past 5d_avg_vol'])
               & (data['pr_chg']<0)),'signal' ]=1

data.loc[((data['pr_chg'].abs() > data['std_100day']) &
          (data['5d_avg_vol']<data['past 5d_avg_vol']) &
          (data['pr_chg']>0)),'signal' ]=-1

data['c_signal']=0
data['exit']=0

for i in range(1,len(data)):
    if((data.iloc[i]['signal'] != 0) & (data.iloc[i]['signal'] != data.iloc[i-1]['c_signal'])) :
        data.iloc[i, data.columns.get_loc('c_signal')] = data.iloc[i, data.columns.get_loc('signal')]
        if data['signal'][i] == 1:
            data.iloc[i,data.columns.get_loc('exit')] = 1
        else:
            data.iloc[i,data.columns.get_loc('exit')]= -1
    if((data['signal'][i]!=0) & (data['signal'][i]== data['c_signal'][i-1])) :
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        if data['c_signal'][i-1]==1:
               data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])+1
        else:
            data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])-1
    if((data['signal'][i]==0)&(data['exit'][i-1]<5)&(data['exit'][i-1]>0)):
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])+1
    if((data['signal'][i]==0)&(data['exit'][i-1]>-5)&(data['exit'][i-1]<0)):
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])-1
    if((data['signal'][i]==0)&((data['exit'][i-1]==5)|(data['exit'][i-1]==-5))):
        data.iloc[i,data.columns.get_loc('c_signal')]=0
        data.iloc[i,data.columns.get_loc('exit')]=0


print(data.tail())

data['return'] = np.log(data['Close']/data['Close'].shift(1))

data['str_return']=data['return']*data['c_signal']

data['cu_str_return']=0
data['cu_mar_return']=0

data.iloc[100:,data.columns.get_loc('cu_str_return')]=pd.expanding_sum(data['str_return'][100:])

data.iloc[100:,data.columns.get_loc('cu_mar_return')]=pd.expanding_sum(data['return'][100:])

data[['cu_mar_return','cu_str_return','c_signal']].tail()

plt.figure(figsize=(10,7))
plt.plot(data['cu_str_return'][100:], color='g',label='Strategy Returns')
plt.plot(data['cu_mar_return'][100:], color='r',label='Market Returns')
plt.legend(loc='best')
plt.show()
(data['cu_str_return'].iloc[-1]-data['cu_mar_return'].iloc[-1])/data['cu_str_return'].std()