from backtesting_numba.backtesting import Backtesting
from backtesting_numba.data_class import DataClass
import pandas as pd
import numpy as np
import pytest
import backtesting_numba.sample_indicators as ind
import backtesting_numba.sample_rules.buy_enter as ber
import backtesting_numba.sample_rules.sell_enter as ser
import backtesting_numba.sample_rules.buy_close as bcr
import backtesting_numba.sample_rules.sell_close as scr


@pytest.fixture
def dataframe_aapl():
    try:
        dataframe = pd.read_csv('../sample_data/AAPL.csv')
    except Exception:
        dataframe = pd.read_csv('backtesting_numba/sample_data/AAPL.csv')

    return dataframe


@pytest.fixture
def dataclass_aapl(dataframe_aapl):
    dataclass = DataClass(dataframe_aapl, with_indicators=True)
    dataclass.delete_indicator('Unnamed: 0')
    return dataclass


@pytest.fixture
def backtesting_aapl(dataclass_aapl):
    return Backtesting(dataclass_aapl)


def test_dataclass_aapl(dataclass_aapl):
    assert dataclass_aapl


def test_backtesting_init(dataclass_aapl, dataframe_aapl):
    back_aapl_1 = Backtesting(dataclass_aapl)
    back_aapl_2 = Backtesting(dataframe_aapl)
    assert isinstance(back_aapl_1.data_class, DataClass) and isinstance(back_aapl_2.data_class, DataClass)


def test_indicator(backtesting_aapl):
    backtesting_aapl.indicator(ind.moving_avarange_df, 20, name='ma_20')
    assert isinstance(backtesting_aapl.data_class.indicators['ma_20'], np.ndarray)


def test_buy_enter(backtesting_aapl):
    backtesting_aapl.indicator(ind.moving_avarange_df, 20, name='ma_fast')
    backtesting_aapl.indicator(ind.moving_avarange_df, 120, name='ma_slow')

    backtesting_aapl.buy_enter(ber.buy_enter_crossover, 'ma_fast', 'ma_slow')
    assert isinstance(backtesting_aapl.data_class.buy_enter, np.ndarray)


def test_sell_enter(backtesting_aapl):
    backtesting_aapl.indicator(ind.moving_avarange_df, 20, name='ma_fast')
    backtesting_aapl.indicator(ind.moving_avarange_df, 120, name='ma_slow')

    backtesting_aapl.sell_enter(ser.sell_enter_crossover, 'ma_fast', 'ma_slow')
    assert isinstance(backtesting_aapl.data_class.sell_enter, np.ndarray)


@pytest.fixture
def backtesting_entrys(backtesting_aapl):
    backtesting_aapl.indicator(ind.moving_avarange_df, 20, name='ma_fast')
    backtesting_aapl.indicator(ind.moving_avarange_df, 120, name='ma_slow')

    backtesting_aapl.buy_enter(ber.buy_enter_crossover, 'ma_fast', 'ma_slow')
    backtesting_aapl.sell_enter(ser.sell_enter_crossover, 'ma_fast', 'ma_slow')

    return backtesting_aapl


def test_backtesting_entrys(backtesting_entrys):
    assert backtesting_entrys


def test_backtesting_buy_close(backtesting_entrys):
    backtesting_entrys.buy_close(bcr.buy_close_after_x, 10)

    assert isinstance(backtesting_entrys.data_class.buy_close, np.ndarray)


def test_backtesting_sell_close(backtesting_entrys):
    backtesting_entrys.sell_close(scr.sell_close_after_x, 10)

    assert isinstance(backtesting_entrys.data_class.sell_close, np.ndarray)


def test_backtesting_crossover_strategy(backtesting_entrys):
    backtesting_entrys.backtesting()
