import os
import pandas as pd
from backtesting_walkfoward.backtesting import Backtesting
import backtesting_walkfoward.sample_indicators as bni
from backtesting_walkfoward.sample_rules import buy_enter, sell_enter

if __name__ == '__main__':
    try:
        os.chdir('backtesting_walkfoward/exemples/exemple_backtesting_strategy')
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

    backtesting.backtesting(revert=True, timeit=True)

    backtesting.data_class.plot_bokeh_indicators(
        line_indicators={'ma_20': 'blue', 'ma_200': 'yellow'},
        circle_indicators={'buy_enter_price': 'green', 'sell_enter_price': 'red'}
    )

    metrics_results = backtesting.results()
