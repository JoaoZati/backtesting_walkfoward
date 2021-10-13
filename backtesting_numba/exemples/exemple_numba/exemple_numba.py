from numba import njit, prange
from backtesting_numba.data_class import DataClass
import pandas as pd
import os
from backtesting_numba.fixtures import timeit
import numpy as np

try:
    os.chdir('backtesting_numba/exemples/exemples_numba')
except Exception:
    pass

path = '../../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)
dataclass_aapl = DataClass(df_aapl)


@timeit
def moving_avarange_df(data_class, n):
    df = data_class.dataframe.copy()

    ma = np.array(df.close.rolling(n).mean())

    return ma


@njit
def move_avarange_njit(close, n):
    ma = np.zeros(len(close))
    for i in prange(len(close)):
        if i < n:
            continue
        ma[i] = close[i - n] / close[i]

    return ma


@timeit
def moving_avarange_njit(data_class, n):
    close = data_class.close

    return move_avarange_njit(close, n)


if __name__ == '__main__':
    moving_avarange_df(dataclass_aapl, 20)
    moving_avarange_njit(dataclass_aapl, 20)
    moving_avarange_njit(dataclass_aapl, 20)
