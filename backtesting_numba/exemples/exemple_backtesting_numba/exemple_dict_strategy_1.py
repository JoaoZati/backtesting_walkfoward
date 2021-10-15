import pandas as pd
from backtesting_numba.data_class import DataClass
from backtesting_numba.backtesting import Backtesting
import backtesting_numba.sample_indicators as ind
import backtesting_numba.sample_rules.buy_entry as ber
import backtesting_numba.sample_rules.sell_entry as ser
import os

if __name__ == '__main__':
    data_sample = {
        'date': ['2021-04-01', '2021-04-02', '2021-04-03', '2021-04-04', '2021-04-05'],
        'open': [5.5, 6, 5.75, 6, 7.5],
        'high': [5.8, 7, 6.75, 7, 8.5],
        'low': [4.5, 5, 4.75, 5, 6.5],
        'close': [5.8, 5, 5.8, 5.8, 6.8],
    }

    backtesting = Backtesting(data_sample)

    def buy_enter(data_class):
        return [0, 6, 0, 6, 0]

    backtesting.buy_enter(buy_enter)
    backtesting.backtesting()
    backtesting.backtesting(comission_enter=0.1, slippage_enter=0.1, buy_stop_loss=True, bsl_value=0.5)
    print(backtesting.data_class.dataframe)
    backtesting.backtesting(
        comission_enter=0.1, slippage_enter=0.1,
        buy_stop_loss=True, bsl_value=0.5,
        buy_trailing_stop=True, bts_value=0.25,
    )
    print(backtesting.data_class.dataframe)
    backtesting.backtesting(
        comission_exit=0.05, slippage_exit=0.05,
        buy_take_profit=True, btp_value=0.25
    )
    print(backtesting.data_class.dataframe)
