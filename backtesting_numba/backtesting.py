from backtesting_numba.data_class import DataClass
# import numpy as np
# import pandas as pd


class Backtesting:

    def __init__(self, data_class, index_date=False, with_indicators=False):
        """
        :param data_class: DataClass object
        """

        if not isinstance(data_class, DataClass):
            try:
                data_class = DataClass(data_class, index_date=index_date, with_indicators=with_indicators)
            except Exception as e:
                print('cold not convert data into DataClass, see DataClass documentation')
                raise e

        self.data_class = data_class

    def indicator(self, func, *args):
        try:
            indicators = func(self.data_class, *args)
            for key, value in indicators.items():
                self.data_class.add_update_indicator(key, value)
        except Exception as e:
            raise e

    def buy_enter(self, func, *args):
        try:
            buy_enter = func(self.data_class, *args)
            self.data_class._set_buy_enter(buy_enter)
        except Exception as e:
            raise e

    def buy_close(self, func, *args):
        try:
            buy_close = func(self.data_class, *args)
            self.data_class._set_buy_close(buy_close)
        except Exception as e:
            raise e
