import numpy as np
import backtesting_numba.errors as er
import pandas as pd


def assert_numpy_date(elements):
    try:
        element = [np.datetime64(i) for i in elements]
        output = np.array(element)
    except Exception as e:
        raise e

    return output


def assert_numpy_elements(element):
    try:
        output = np.array(element)
    except Exception as e:
        raise e

    if output.dtype != float and output.dtype != int and output.dtype != bool:
        print(output.dtype)
        raise er.ArrayNotFloats

    return output


class DataClass:
    """
    Class used as data in the backtesting process

    :arg data_input: a dataframe, dictionary or instance that can be converted in dataframe with columns:
    date (datetime),
    open (int or float),
    high (int or float),
    low (int or float),
    close (int or float).

    All NaN values are dropped.
    """

    def __init__(self, data_input, index_date=False, with_indicators=False):

        self._columns_index_false = ['date', 'open', 'high', 'low', 'close']
        self._columns_index_true = ['open', 'high', 'low', 'close']

        if not isinstance(data_input, pd.DataFrame):
            index_date = False

            try:
                data_input = pd.DataFrame(data_input)
            except Exception as e:
                raise e

        columns_index = self._columns_index_false
        if index_date:
            columns_index = self._columns_index_true

        for column in columns_index:
            if column not in data_input.columns:
                print(f'Data frame must have "{column}" as column, be sure all letters is lowered')
                raise er.MissingColumn

        data_input.dropna(inplace=True)

        self.open = assert_numpy_elements(data_input.open)
        self.high = assert_numpy_elements(data_input.high)
        self.low = assert_numpy_elements(data_input.low)
        self.close = assert_numpy_elements(data_input.close)
        self._dict_candle = {
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

        if index_date:
            self.date = assert_numpy_date(data_input.index)
        else:
            self.date = assert_numpy_date(data_input.date)

        self.indicators = {}
        if with_indicators:
            exclude_columns = self._columns_index_false
            if index_date:
                exclude_columns = self._columns_index_true
            data_indicators = data_input.loc[:, [i for i in list(data_input.columns) if i not in exclude_columns]]

        for column in data_indicators.columns:
            self.indicators[column] = assert_numpy_elements(data_indicators[column])

    def update_dict_candle(self):
        self._dict_candle = {
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }


if __name__ == '__main__':
    data = DataClass(open=[0, 1, 2])
