import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas.io.data as web

### Monte Carlo Valuation Of European Call Option

s0 = 100
K = 105
T = 1.0
r = 0.05
sigma = 0.2

I = 100000
z = np.random.standard_normal(I)
ST = s0 * np.exp((r - 0.05 * sigma**2)*T + sigma * np.sqrt(T)*z)

hT = np.maximum(ST - K,0)
C0 = np.exp(-r *T)*sum(hT)/I

print('Value os the European Call Option %5.3f') % C0