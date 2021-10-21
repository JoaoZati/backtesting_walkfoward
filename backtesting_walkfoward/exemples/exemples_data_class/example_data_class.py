from backtesting_walkfoward.data_class import DataClass

data_sample_with_indicators = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 4.75],
    'close': [5.8, 5, 5.8],
    'ma25': [7, 7.25, 6.55],
    'renko': [9, 9.25, 5.55]
}

data_class = DataClass(data_sample_with_indicators)
data_class_indicators = DataClass(data_sample_with_indicators, with_indicators=True)


if __name__ == '__main__':
    print(data_class.date)
    print(type(data_class.date))
    print(type(data_class.date[0]))
    print(data_class.open)
    print(type(data_class.open))
    print(data_class.dataframe)
    print(type(data_class.dataframe))
    print(data_class_indicators.dataframe)
    print(type(data_class_indicators.dataframe))
