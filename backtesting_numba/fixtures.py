import time
from numba import njit


def timeit(func):
    def timebegend(*args, **kwargs):
        time1 = time.time()
        value = func(*args, **kwargs)
        time2 = time.time()
        print('function took {:.3f} ms'.format((time2 - time1) * 1000.0))
        return value

    return timebegend


def numba_njit_ohlc(func):
    def init(dataclass, *args, **kwargs):
        open = dataclass.open
        high = dataclass.high
        low = dataclass.low
        close = dataclass.close
        value = njit(func(open, high, low, close, *args, **kwargs))
        return value

    return init


def add1_a(func):
    def init(a, *args, **kwargs):
        print(a)
        a += 1
        print(a)
        value = func(a, *args, **kwargs)
        return value

    return init


if __name__ == '__main__':
    @timeit
    def calculate_number(number):
        time.sleep(number)

    calculate_number(5)

    @add1_a
    def soma(a, b, c):
        return a + b + c

    print(soma(1, 2, 3))
