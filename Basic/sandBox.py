import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bsm_formula_IV import *

# source: https://github.com/yhilpisch/py4fi/tree/master/ipython/source
h5 = pd.HDFStore('vstoxx_data_31032014.h5', 'r')
futures_data = h5['futures_data']
options_data = h5['options_data']
h5.close()

# futures_data
# options_data.info()

# print options_data[['DATE', 'MATURITY', 'TTM', 'STRIKE', 'PRICE']].head()

options_data['IMP_VOL'] = 0.0

tol = 0.5
V0 = 17.6639
r = 0.01

for option in options_data.index:
    forward = futures_data[futures_data['MATURITY'] == options_data.loc[option]['MATURITY']]['PRICE'].values[0]
    if (forward * (1 - tol) < options_data.loc[option]['STRIKE'] < forward * (1 + tol)):
        imp_vol = bsm_call_imp_vol(S0 = V0,
                               K = options_data.loc[option]['STRIKE'],
                               T = options_data.loc[option]['TTM'],
                               r = r,
                               sigma_est = 2.0,
                               C0 = options_data.loc[option]['PRICE'],
                               it = 100)
        options_data['IMP_VOL'].loc[option] = imp_vol

# print futures_data['MATURITY']

# print options_data.loc[46170]

to_plot = options_data[options_data['IMP_VOL'] > 0]

maturities = sorted(set(options_data['MATURITY']))
print maturities


plt.figure(figsize=(8, 6))
for maturity in maturities:
    data = to_plot[options_data.MATURITY == maturity]
    plt.plot(data['STRIKE'], data['IMP_VOL'],
             label= maturity.date(), lw = 1.5)
    plt.plot(data['STRIKE'], data['IMP_VOL'], 'r.')
plt.grid(True)
plt.xlabel('Strike')
plt.ylabel('Implied Volatility of Volatility')
plt.legend()
plt.show()


keep = ['PRICE', 'IMP_VOL']
group_data = to_plot.groupby(['MATURITY', 'STRIKE'])[keep]
group_data = group_data.sum()
print group_data.head()