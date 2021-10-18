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


def sell_enter_crossover(dataclass, ma_fast: str, ma_slow: str):
    ma_fast = dataclass.indicators[ma_fast]
    ma_slow = dataclass.indicators[ma_slow]
    open = dataclass.open

    sell_enter = sell_enter_crossover_njit(ma_fast, ma_slow, open)
    return sell_enter
