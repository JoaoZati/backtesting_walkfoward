from numba import njit
import numpy as np


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
