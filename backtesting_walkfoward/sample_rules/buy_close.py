from numba import njit
import numpy as np


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
