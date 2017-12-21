import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pandas_datareader import data, wb
import quandl


class bsm_call_IV(object):


    def __init__(self, S0, K, T, r, sigma, C0, it=100):

        self.S0 = np.float(S0)
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.vega = None
        self.value = None
        self.C0 = C0
        # self.sigma_est = sigma_est
        self.it = it
        # self.bsm_call_value()
        # self.bsm_vega()


    def bsm_call_value(self):
        '''
        :param S0: Initial Stock
        :param K: Striike price
        :param T: Maturity date
        :param r: constant risk-free short rate
        :param sigma: volatility
        :return: Present value of the european call option
        '''

        # S0 = np.float(S0)
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S0 / self.K) + (self.r - 0.5 * self.sigma**2) * self.T)/(self.sigma * np.sqrt(self.T))
        self.value = (self.S0 * stats.norm.cdf(d1, 0.0, 1.0) - np.exp(-self.r * self.T) * self.K * stats.norm.cdf(d2, 0.0, 1.0))

        return self.value

    def bsm_vega(self):
        '''

        :param S0:
        :param K:
        :param T:
        :param r:
        :param sigma:
        :return:
        '''

        # S0 = np.float(S0)
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        self.vega = self.S0 * stats.norm.cdf(d1, 0.0, 1.0) * np.sqrt(self.T)

        return self.vega

    def bsm_call_imp_vol(self):
        # type: () -> object
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

        for i in range(self.it):
            self.sigma -= ((self.value - self.C0) / self.vega)
            return self.sigma

if __name__ == '__main__':
    v =  bsm_call_IV(S0=10, K=15, T=1, r=0.01, sigma=17.6639, C0=0.5)
    print v.bsm_vega()
    print v.bsm_call_value()
    print v.bsm_call_imp_vol()

