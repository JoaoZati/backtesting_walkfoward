import numpy as np
import backtesting_numba.errors as er


class DataClass:
    """
    Class used as data in the backtesting process

    :arg dataframe: a dataframe with columns: date (date of candle, datetime), open, high, low, close (all floats).
    :arg open: float
    :arg high: float
    :arg low: float
    :arg close: float
    """

    def __init__(self, dataframe=None, open=None, high=None, low=None, close=None, date=None):
        if open:
            try:
                self.open = np.array(open)
            except Exception as e:
                print(e)
                return
            if len(self.open.shape) != 1:
                print('1')
                raise er.NotOneColumn
            if self.open.dtype != float or self.open.dtype != int:
                print('2')
                raise er.ArrayNotFloats


        if dataframe:
            pass


if __name__ == '__main__':
    data = DataClass(open=[0, 1, 2])