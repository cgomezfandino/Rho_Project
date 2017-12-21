from math import *
import numpy as np
import time
import numexpr as ne


# 1
loops = 25000000
a = range(1, loops)

def f(x):
    return 3 * np.log(x) + np.cos(x)**2

# compilinig in math
st = time.time()
r = [f(x) for x in a]
ft = time.time()-st
print('processing time %5.3f Seconds' %ft) # 78.64 Seconds

# compiling in numpy
a = np.arange(1, loops)
st2 = time.time()
r = 3 * np.log(a) + np.cos(a) **2
ft2= time.time()-st2
print('processing time %5.3f Seconds' %ft2) # 2.49 Seconds


# With one Thread

ne.set_num_threads(1)
st3 = time.time()
f = '3 * log(a) + cos(a) **2'
ft3 = time.time() - st3
print('processing time %5.3f Seconds' %ft3) # 0.00 Seconds

# With four Threads
ne.set_num_threads(4)
st4 = time.time()
f = '3 * log(a) + cos(a) **2'
ft4 = time.time() - st3
print('processing time %5.3f Seconds' %ft4) # 0.00 Seconds

# %timeit
