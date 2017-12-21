import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pandas_datareader import data, wb
import quandl


def bsm_call_value(S0, K, T, r, sigma):
    '''
    :param S0: Initial Stock
    :param K: Striike price
    :param T: Maturity date
    :param r: constant risk-free short rate
    :param sigma: volatility
    :return: Present value of the european call option
    '''

    S0 = np.float(S0)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S0 / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    value = (S0 * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))

    return value

def bsm_vega(S0, K, T, r, sigma):
    '''

    :param S0:
    :param K:
    :param T:
    :param r:
    :param sigma:
    :return:
    '''

    S0 = np.float(S0)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2)) * T / (sigma * np.sqrt(T))
    vega = S0 * stats.norm.cdf(d1, 0.0, 1.0) * np.sqrt(T)

    return vega

def bsm_call_imp_vol(S0, K, T, r, C0, sigma_est, it=100):
    ''' Implied Volatility of European Vall option in BSM Model

    :param S0:
    :param K:
    :param T:
    :param r:
    :param C0:
    :param sigma_est:
    :param it:
    :return:
    '''

    for i in range(it):
        sigma_est -= ((bsm_call_value(S0, K, T, r, sigma_est) - C0) / bsm_vega(S0, K, T, r, sigma_est))
        return sigma_est

if __name__ == '__main__':
    v = bsm_call_imp_vol(S0=10, K=15, T=1, r=0.01, sigma_est=17.6639, C0=0.5)
    print v

