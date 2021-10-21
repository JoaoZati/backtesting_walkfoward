from backtesting_walkfoward.backtesting import Backtesting
import pandas as pd
import os
from backtesting_walkfoward.exemples.exemple_numba.exemple_numba import moving_avarange_df
from numba import njit
import numpy as np


@njit(parallel=True)
def sell_enter_crossover_njit(mf, ms, op):
    se = np.zeros(len(mf))

    for i in range(len(se)):
        if i < 2:
            continue
        if not mf[i] or not ms[i]:
            continue
        if mf[i - 2] >= ms[i - 2] and mf[i - 1] < ms[i - 1]:
            se[i] = op[i]

    return se


def sell_enter_crossover(dataclass):
    ma_fast = dataclass.indicators['ma_fast']
    ma_slow = dataclass.indicators['ma_slow']
    open = dataclass.open

    sell_enter = sell_enter_crossover_njit(ma_fast, ma_slow, open)
    return sell_enter


@njit(parallel=True)
def sell_close_after_x_njit(se, op, x):
    sc = np.zeros(len(se))

    for i in range(len(se)):
        if i < x:
            continue
        if se[i - x]:
            sc[i] = op[i]

    return sc


def sell_close_after_x(dataclass, x):
    if dataclass.sell_enter is None:
        print('Sell Enter is None')
        raise ValueError

    sell_enter = dataclass.sell_enter if dataclass.sell_enter is not None else False
    open = dataclass.open

    sell_close = sell_close_after_x_njit(sell_enter, open, x)
    return sell_close


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

    backtesting.sell_enter(sell_enter_crossover)

    backtesting.sell_close(sell_close_after_x, 10)

    df = backtesting.data_class.dataframe
