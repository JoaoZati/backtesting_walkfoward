import pytest
from backtesting_walkfoward import download_data as dd
import datetime as dt
import backtesting_walkfoward.errors as er


class MockDownload(dd.DownloadData):
    def __init__(self, ticker, start_date=dt.datetime.now() - dt.timedelta(3600), end_date=dt.datetime.now(),
                 site_scrapy='yfinance', timeframe='1d', size='full',
                 key_path=''):
        super().__init__(ticker, start_date, end_date,
                         site_scrapy, timeframe, size,
                         key_path)

    def get_yfinance_data(self):
        return 1

    def get_alphavantage_data(self):
        return 2, 1


ticker = 'MSFT'
list_ticker = ['MSFT', 'AAPL']
list_ticker_wrong = [0, True]


@pytest.mark.parametrize(
    'ticker',
    list_ticker
)
def test_ticker(ticker):
    mock_data = MockDownload(ticker=ticker)
    assert mock_data.ticker == ticker


@pytest.mark.parametrize(
    'ticker',
    list_ticker_wrong
)
def test_ticker_wrong(ticker):
    with pytest.raises(ValueError):
        MockDownload(ticker=ticker)


def test_datetime_istance():
    mock_data = MockDownload(ticker)
    print(mock_data.start_date)
    assert isinstance(mock_data.start_date, dt.datetime) and \
           isinstance(mock_data.end_date, dt.datetime)


def test_datetime_after():
    with pytest.raises(er.EndDateBeforeStartDate):
        MockDownload(ticker, start_date=dt.datetime.now(), end_date=dt.datetime.now() - dt.timedelta(100))


list_site_scrapy = ['yfinance', 'alphavantage']
list_site_scrapy_wrong = ['yfinancee', 'alphavantagee']


@pytest.mark.parametrize(
    'site_scrapy',
    list_site_scrapy
)
def test_site_scrapy(site_scrapy):
    mock_data = MockDownload(ticker, site_scrapy=site_scrapy)
    assert mock_data.site_scrapy == site_scrapy


@pytest.mark.parametrize(
    'site_scrapy',
    list_site_scrapy_wrong
)
def test_site_scrapy_wrong(site_scrapy):
    with pytest.raises(er.NotinList):
        MockDownload(ticker, site_scrapy=site_scrapy)


list_size = ['full', 'compact']
list_size_wrong = ['fulll', 1]


@pytest.mark.parametrize(
    'size',
    list_size
)
def test_size(size):
    mock_data = MockDownload(ticker, size=size)
    assert mock_data.size == size


@pytest.mark.parametrize(
    'size',
    list_size_wrong
)
def test_size_wrong(size):
    with pytest.raises(er.NotinList):
        MockDownload(ticker, size=size)


list_key_path = ['/home/joao', '']
list_key_path_wrong = [15, True]


@pytest.mark.parametrize(
    'key_path',
    list_key_path
)
def test_key_path(key_path):
    mock_data = MockDownload(ticker, key_path=key_path)
    assert mock_data.key_path == key_path


@pytest.mark.parametrize(
    'key_path',
    list_key_path_wrong
)
def test_key_path_wrong(key_path):
    with pytest.raises(ValueError):
        MockDownload(ticker, key_path=key_path)


list_timeframe = ['1d']
list_timeframe_wrong = ['5d']


@pytest.mark.parametrize(
    'timeframe',
    list_timeframe
)
def test_timeframe(timeframe):
    mock_data = MockDownload(ticker, timeframe=timeframe)
    assert mock_data.timeframe == timeframe


@pytest.mark.parametrize(
    'timeframe',
    list_timeframe_wrong
)
def test_timeframe_wrong(timeframe):
    with pytest.raises(er.NotinList):
        MockDownload(ticker, site_scrapy='alphavantage', timeframe=timeframe)
