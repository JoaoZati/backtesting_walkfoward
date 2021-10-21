from numba import njit, prange
import pandas as pd
import os
from backtesting_walkfoward.fixtures import timeit
import numpy as np

try:
    os.chdir('backtesting_walkfoward/exemples/exemples_numba')
except Exception:
    pass


@timeit
def diff(DF):
    df = DF.copy()
    diff = 0
    l_diff = [0]

    for i in range(1, len(df)):
        if df['close'][i] > df['close'][i - 1]:
            l_diff.append(diff)
            diff = 0
        else:
            diff += 1
            l_diff.append(diff)

    return np.array(l_diff)


@timeit
def numpy_diff(DF):
    df = DF.copy()
    diff = 0
    cl = np.array(df['close'])
    af = np.zeros(len(cl))

    for i in range(1, len(cl)):
        if cl[i] > cl[i - 1]:
            af[i] = diff
            diff = 0
        else:
            diff += 1
            af[i] = diff

    return af


@njit(parallel=True)
def numba_diff(cl, af):
    diff = 0

    for i in prange(1, len(cl)):
        if cl[i] > cl[i - 1]:
            af[i] = diff
            diff = 0
        else:
            diff += 1
            af[i] = diff

    return af


@timeit
def df_diff_numba(DF):
    df = DF.copy()
    cl = np.array(df['close'])
    af = np.zeros(len(cl))

    sl = numba_diff(cl, af)

    return sl


@timeit
def df_diff_numba_2(DF):
    df = DF.copy()
    cl = np.array(df['open'])
    af = np.zeros(len(cl))

    sl = numba_diff(cl, af)

    return sl


if __name__ == '__main__':
    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    diff(df_aapl)
    numpy_diff(df_aapl)
    df_diff_numba(df_aapl)
    df_diff_numba_2(df_aapl)
