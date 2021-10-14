from backtesting_numba.data_class import DataClass
import numpy as np
from numba import njit


# import pandas as pd


@njit(parallel=True)
def backtesting_numba(
        op, hi, lo, cl,
        be, bc,
        se, sc,
        c_enter, c_exit, s_enter, s_exit,
        btl, bsl_atr, bsl_value,
        btp, btp_atr, btp_value,
        bts, bts_atr, bts_value,
        ssl, ssl_atr, ssl_value,
        stp, stp_atr, stp_value,
        sts, sts_atr, sts_value,
        revert, signal,
        bc_last, sc_last,
):

    short_long, enter_price, exit_price, stop_loss_level, take_profit_level, traling_stop_level = [np.zeros(len(op))]*6
    stop_loss, take_profit, trailing_stop = [0]*3

    return short_long, enter_price, exit_price, stop_loss_level, take_profit_level, traling_stop_level


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

    def indicator(self, func, *args, **kwargs):
        try:
            indicators = func(self.data_class, *args, **kwargs)
            for key, value in indicators.items():
                self.data_class.add_update_indicator(key, value)
        except Exception as e:
            raise e

    def buy_enter(self, func, *args, **kwargs):
        try:
            buy_enter = func(self.data_class, *args, **kwargs)
            self.data_class._set_buy_enter(buy_enter)
        except Exception as e:
            raise e

    def buy_close(self, func, *args, **kwargs):
        try:
            buy_close = func(self.data_class, *args, **kwargs)
            self.data_class._set_buy_close(buy_close)
        except Exception as e:
            raise e

    def sell_enter(self, func, *args, **kwargs):
        try:
            sell_enter = func(self.data_class, *args, **kwargs)
            self.data_class._set_sell_enter(sell_enter)
        except Exception as e:
            raise e

    def sell_close(self, func, *args, **kwargs):
        try:
            sell_close = func(self.data_class, *args, **kwargs)
            self.data_class._set_sell_close(sell_close)
        except Exception as e:
            raise e

    def backtesting(
            self,
            comission_enter=0, comission_exit=0, slippage_enter=0, slippage_exit=0,
            buy_stop_loss=False, bsl_atr=True, bsl_value=2,
            buy_take_profit=False, btp_atr=True, btp_value=2,
            buy_trailing_stop=False, bts_atr=True, bts_value=2,
            sell_stop_loss=False, ssl_atr=True, ssl_value=2,
            sell_take_profit=False, stp_atr=True, stp_value=2,
            sell_trailing_stop=False, sts_atr=True, sts_value=2,
            revert=False, signal=0,
            buy_close_last=False, sell_close_last=False,
    ):
        len_data = len(self.data_class.dataframe)

        if self.data_class.buy_enter is None:
            self.data_class.buy_enter = np.zeros(len_data)

        if self.data_class.buy_close is None:
            self.data_class.buy_close = np.zeros(len_data)

        if self.data_class.sell_enter is None:
            self.data_class.sell_enter = np.zeros(len_data)

        if self.data_class.sell_close is None:
            self.data_class.sell_close = np.zeros(len_data)

        short_long, enter_price, exit_price, stop_loss_level, take_profit_level, traling_stop_level = \
            backtesting_numba(
                self.data_class.open, self.data_class.high, self.data_class.low, self.data_class.close,
                self.data_class.buy_enter, self.data_class.buy_close,
                self.data_class.sell_enter, self.data_class.sell_close,
                comission_enter, comission_exit, slippage_enter, slippage_exit,
                buy_stop_loss, bsl_atr, bsl_value,
                buy_take_profit, btp_atr, btp_value,
                buy_trailing_stop, bts_atr, bts_value,
                sell_stop_loss, ssl_atr, ssl_value,
                sell_take_profit, stp_atr, stp_value,
                sell_trailing_stop, sts_atr, sts_value,
                revert, signal,
                buy_close_last, sell_close_last,
            )
