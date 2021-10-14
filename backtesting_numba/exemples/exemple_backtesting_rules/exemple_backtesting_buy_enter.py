from backtesting_numba.backtesting import Backtesting
import pandas as pd
import os
from backtesting_numba.exemples.exemple_numba.exemple_numba import moving_avarange_df
from numba import njit
import numpy as np

try:
    os.chdir('backtesting_numba/exemples/exemple_backtesting_rules')
    print('ok')
except Exception:
    pass

path = '../../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)

backtesting = Backtesting(df_aapl)
backtesting.indicator(moving_avarange_df, 20, 120)


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


backtesting.buy_enter(buy_enter_crossover)
print(backtesting.data_class.buy_enter)
