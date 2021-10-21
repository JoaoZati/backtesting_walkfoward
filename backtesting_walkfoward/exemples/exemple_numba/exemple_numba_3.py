from numba import jit
import numpy as np
from backtesting_walkfoward.fixtures import timeit

x = np.arange(100).reshape(10, 10)


@timeit
@jit(nopython=True)  # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(a):  # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):  # Numba likes loops
        trace += np.tanh(a[i, i])  # Numba likes NumPy functions
    return a + trace  # Numba likes NumPy broadcasting


[go_fast(x) for _ in range(5)]
