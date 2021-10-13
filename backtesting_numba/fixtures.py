import time


def timeit(func):
    def timebegend(*args, **kwargs):
        time1 = time.time()
        value = func(*args, **kwargs)
        time2 = time.time()
        print('function took {:.3f} ms'.format((time2 - time1) * 1000.0))
        return value

    return timebegend


def numba_indicator_ohlc(func):
    def init(*args, **kwargs):
        value = func(*args, **kwargs)
        return value

    return init


if __name__ == '__main__':
    @timeit
    def calculate_number(number):
        time.sleep(number)

    calculate_number(5)
