import numba
import pytest
import numpy as np
from backtesting_numba.data_class import DataClass
import backtesting_numba.errors as er


@pytest.mark.parametrize(
    'open',
    [[1, 2, 3],
     [12.5, 12.25, 13.265, 14],
     ]
)
def test_open_input(open):
    data = DataClass(open=open)
    assert isinstance(data.open, np.ndarray)


@pytest.mark.parametrize(
    'open',
    [['a', 1, 2]]
)
def test_open_notfloats(open):
    with pytest.raises(er.ArrayNotFloats):
        DataClass(open=open)


@pytest.mark.parametrize(
    'open',
    [[[0, 1, 2], [0, 2, 4]]]
)
def test_open_notfloats(open):
    with pytest.raises(er.NotOneColumn):
        DataClass(open=open)
