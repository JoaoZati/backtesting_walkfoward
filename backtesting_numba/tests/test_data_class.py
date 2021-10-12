import pytest
import numpy as np
from backtesting_numba.data_class import DataClass, assert_numpy_elements, assert_numpy_date
import backtesting_numba.errors as er
import pandas as pd


@pytest.mark.parametrize(
    'open',
    [[1, 2, 3],
     [12.5, 12.25, 13.265, 14],
     ]
)
def test_open_input(open):
    data = assert_numpy_elements(open)
    assert isinstance(data, np.ndarray)


@pytest.mark.parametrize(
    'open',
    [['a', 1, 2]]
)
def test_open_not_floats(open):
    with pytest.raises(er.ArrayNotFloats):
        assert_numpy_elements(open)


data_sample = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 6.75],
    'close': [5.8, 5, 6.75]
}

data_sample_2 = {
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 6.75],
    'close': [5.8, 5, 6.75]
}

data_sample_3 = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'Open': [5.5, 6, 5.75],
    'High': [5.8, 7, 6.75],
    'Low': [4.5, 5, 6.75],
    'Close': [5.8, 5, 6.75]
}

data_sample_4 = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 6.75],
    'close': [5.8, 5]
}


@pytest.mark.parametrize(
    'data',
    [data_sample]
)
def test_dict_input(data):
    assert DataClass(data)


@pytest.mark.parametrize(
    'data',
    [data_sample_4]
)
def test_dict_input_dropna(data):
    with pytest.raises(ValueError):
        data = DataClass(data)


@pytest.mark.parametrize(
    'data',
    [data_sample_2]
)
def test_dict_input_no_date(data):
    with pytest.raises(er.MissingColumn):
        DataClass(data, index_date=True)


@pytest.mark.parametrize(
    'data',
    [data_sample_3]
)
def test_dict_input_no_date_2(data):
    with pytest.raises(er.MissingColumn):
        DataClass(data, index_date=True)


@pytest.mark.parametrize(
    'data',
    [data_sample]
)
def test_dict_input_2(data):
    data_class = DataClass(data)
    bool_isinstance = True
    for value in data_class._dict_candle.values():
        if not isinstance(value, np.ndarray):
            bool_isinstance = False
    assert bool_isinstance


array_test_assert = np.array(
    ['2025-05-01', '2025-06-03', '2025-12-15']
)


@pytest.mark.parametrize(
    'array',
    [array_test_assert]
)
def test_numpy_date(array):
    output = assert_numpy_date(array)
    print(output.dtype)
    assert isinstance(output, np.ndarray) and isinstance(output[0], np.datetime64)


data_sample_indicators = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 4.75],
    'close': [5.8, 5, 5.8],
    'ma25': [7, 7.25, 6.55]
}


@pytest.mark.parametrize(
    'data_input',
    [data_sample_indicators]
)
def test_dataclass_indicators(data_input):
    data = DataClass(data_input, with_indicators=True)
    assert isinstance(data.indicators['ma25'], np.ndarray)


@pytest.mark.parametrize(
    'data_input',
    [data_sample_indicators]
)
def test_dataclass_update_indicator(data_input):
    data = DataClass(data_input, with_indicators=True)
    indicators = {
        'ma25': [8, 8.25, 8.55],
        'ma50': [9, 9.25, 9.55]
    }
    bool_assert = True
    for key, value in indicators.items():
        data.add_update_indicator(key, value)
        print(data.indicators[key])
        for i, item in enumerate(value):
            if not data.indicators[key][i] == item:
                bool_assert = False

    assert bool_assert


data_sample_indicators_2 = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 4.75],
    'close': [5.8, 5, 5.8],
    'ma25': [7, 7.25, 6.55],
    'renko': [9, 9.25, 5.55]
}


@pytest.mark.parametrize(
    'data_input',
    [data_sample_indicators_2]
)
def test_dataclass_dataframe(data_input):
    data = DataClass(data_input, with_indicators=True)
    bool_assert = True
    for key in data_input.keys():
        if key not in data.dataframe.columns:
            bool_assert = False
    assert isinstance(data.dataframe, pd.DataFrame) and bool_assert
