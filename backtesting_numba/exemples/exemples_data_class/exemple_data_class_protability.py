from backtesting_numba.data_class import DataClass # noqa
import os
import pandas as pd
from backtesting_numba.backtesting import Backtesting
import backtesting_numba.sample_indicators as bni
from backtesting_numba.sample_rules import buy_enter, sell_enter
import backtesting_numba.sample_kpi as kpi

if __name__ == '__main__':
    try:
        os.chdir('backtesting_numba/exemples/exemple_backtesting_strategy')
        print('ok')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    backtesting = Backtesting(df_aapl)

    backtesting.indicator(bni.moving_avarange_df, 20, 'ma_20')
    backtesting.indicator(bni.moving_avarange_df, 200, 'ma_200')
    backtesting.buy_enter(buy_enter.buy_enter_crossover, 'ma_20', 'ma_200')
    backtesting.sell_enter(sell_enter.sell_enter_crossover, 'ma_20', 'ma_200')

    backtesting.backtesting(revert=True)

    kpi_df = kpi.df_metrics(backtesting.data_class)