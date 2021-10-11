import numba
import pytest
import numpy as np
from backtesting_numba.data_class import DataClass, assert_numpy
import backtesting_numba.errors as er


@pytest.mark.parametrize(
    'open',
    [[1, 2, 3],
     [12.5, 12.25, 13.265, 14],
     ]
)
def test_open_input(open):
    data = assert_numpy(open)
    assert isinstance(data, np.ndarray)


@pytest.mark.parametrize(
    'open',
    [['a', 1, 2]]
)
def test_open_not_floats(open):
    with pytest.raises(er.ArrayNotFloats):
        assert_numpy(open)


data_sample = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 6.75],
    'close': [5.8, 5, 6.75]
}


@pytest.mark.parametrize(
    'data',
    [data_sample]
)
def test_dict_input(data):
    assert DataClass(data)
