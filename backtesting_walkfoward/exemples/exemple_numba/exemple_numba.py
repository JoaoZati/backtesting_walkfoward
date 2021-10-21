from numba import njit, prange
from backtesting_walkfoward.data_class import DataClass
import pandas as pd
import os
from backtesting_walkfoward.fixtures import timeit
import numpy as np


@timeit
def moving_avarange_df(data_class, n, m):
    df = data_class.dataframe.copy()

    ma_f = np.array(df.close.rolling(n).mean())
    ma_s = np.array(df.close.rolling(m).mean())

    return {'ma_fast': ma_f, 'ma_slow': ma_s}


@njit
def move_avarange_njit(close, n):
    ma = np.zeros(len(close))
    for i in prange(len(close)):
        if i < n:
            continue
        close_range = close[i - n: i]
        ma[i] = np.sum(close_range) / len(close_range)

    return ma


@timeit
def moving_avarange_njit(data_class, X, Y):
    close = data_class.close

    ma_X = move_avarange_njit(close, X)
    ma_Y = move_avarange_njit(close, Y)

    return {'ma_fast': ma_X, 'ma_slow': ma_Y}


if __name__ == '__main__':
    try:
        os.chdir('backtesting_walkfoward/exemples/exemples_numba')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)
    dataclass_aapl = DataClass(df_aapl)

    print(moving_avarange_df(dataclass_aapl, 20))
    print(moving_avarange_njit(dataclass_aapl, 20, 50))
    print(moving_avarange_njit(dataclass_aapl, 50, 120))
