# from backtesting_numba.backtesting import Backtesting
from backtesting_numba.data_class import DataClass
import pandas as pd
import pytest


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


def test_dataclass_aapl(dataclass_aapl):
    assert dataclass_aapl
