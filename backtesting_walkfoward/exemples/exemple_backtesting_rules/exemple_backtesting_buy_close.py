from backtesting_walkfoward.backtesting import Backtesting
import pandas as pd
import os
from backtesting_walkfoward.exemples.exemple_numba.exemple_numba import moving_avarange_df
from numba import njit
import numpy as np


@njit(parallel=True)
def buy_enter_crossover_njit(mf, ms, op):
    be = np.zeros(len(mf))

    for i in range(len(be)):
        if i < 2:
            continue
        if not mf[i] or not ms[i]:
            continue
        if mf[i - 2] <= ms[i - 2] and mf[i - 1] > ms[i - 1]:
            be[i] = op[i]

    return be


def buy_enter_crossover(dataclass):
    ma_fast = dataclass.indicators['ma_fast']
    ma_slow = dataclass.indicators['ma_slow']
    open = dataclass.open

    buy_enter = buy_enter_crossover_njit(ma_fast, ma_slow, open)
    return buy_enter


@njit(parallel=True)
def buy_close_after_x_njit(be, op, x):
    bc = np.zeros(len(be))

    for i in range(len(be)):
        if i < x:
            continue
        if be[i - x]:
            bc[i] = op[i]

    return bc


def buy_close_after_x(dataclass, x):
    if dataclass.buy_enter is None:
        print('Buy Enter is None')
        raise ValueError

    buy_enter = dataclass.buy_enter if dataclass.buy_enter is not None else False
    open = dataclass.open

    buy_close = buy_close_after_x_njit(buy_enter, open, x)
    return buy_close


if __name__ == '__main__':
    try:
        os.chdir('backtesting_walkfoward/exemples/exemple_backtesting_rules')
        print('ok')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    backtesting = Backtesting(df_aapl)
    backtesting.indicator(moving_avarange_df, 20, 120)

    backtesting.buy_enter(buy_enter_crossover)
    print(backtesting.data_class.buy_enter)

    backtesting.buy_close(buy_close_after_x, 10)

    df = backtesting.data_class.dataframe
