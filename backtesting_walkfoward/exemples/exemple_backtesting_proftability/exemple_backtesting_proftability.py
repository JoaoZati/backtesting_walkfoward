from backtesting_walkfoward.data_class import DataClass # noqa
import os
import pandas as pd
from backtesting_walkfoward.backtesting import Backtesting
import backtesting_walkfoward.sample_indicators as bni
from backtesting_walkfoward.sample_rules import buy_enter, sell_enter

if __name__ == '__main__':
    try:
        os.chdir('backtesting_walkfoward/exemples/exemple_backtesting_proftability')
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

    output = backtesting.results(silent=True)
    df_kpi = backtesting.df_metrics

    return_crossover_year = (output['return'] / 22) * 100
    return_buyandhold_year = ((df_aapl.close.iloc[-1]/df_aapl.close.iloc[0] - 1) / 12) * 100
