import pandas as pd
from backtesting_numba.data_class import DataClass
from backtesting_numba.backtesting import Backtesting
import backtesting_numba.sample_indicators as ind
import backtesting_numba.sample_rules.buy_enter as ber
import backtesting_numba.sample_rules.sell_enter as ser


if __name__ == '__main__':
    try:
        dataframe = pd.read_csv('../../sample_data/AAPL.csv')
    except Exception:
        dataframe = pd.read_csv('backtesting_numba/sample_data/AAPL.csv')

    dataclass = DataClass(dataframe, with_indicators=True)
    dataclass.delete_indicator('Unnamed: 0')

    backtesting = Backtesting(dataclass)

    backtesting.indicator(ind.moving_avarange_df, 20, name='ma_fast')
    backtesting.indicator(ind.moving_avarange_df, 120, name='ma_slow')

    backtesting.buy_enter(ber.buy_enter_crossover, 'ma_fast', 'ma_slow')
    backtesting.sell_enter(ser.sell_enter_crossover, 'ma_fast', 'ma_slow')

    backtesting.backtesting(timeit=True)
    backtesting.backtesting(timeit=True)
    backtesting.backtesting(timeit=True)
