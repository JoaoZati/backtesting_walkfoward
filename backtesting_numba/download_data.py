import pandas as pd
import datetime as dt
import backtesting_numba.errors as er
import yfinance as yf


class DownloadData:
    _list_sites_scrapy = ['yfinance', 'alphavantage']
    _list_sizes_alphavantage = ['full', 'compact']
    dataframe = None

    def __init__(self, ticker, start_date=dt.datetime.now() - dt.timedelta(3600), end_date=dt.datetime.now(),
                 site_scrapy='yfinance', timeframe='1d', size='full',
                 key_path='') -> pd.DataFrame:
        """

        :param start_date: datetime of beggining of scrapy.
        :param end_date: datetime of ending of scrapy
        :param site_scrapy: str sites can be used in this class, use self.
        :param interval: str timeframe of respective scrapy site for the candles
        :param size: str used for alphavantage to scrap
        """
        if not isinstance(ticker, str):
            print('ticker should be a str with name of asset you want download')
            raise ValueError

        if not isinstance(start_date, dt.datetime) or not isinstance(end_date, dt.datetime):
            print('instance should be a datetime')
            raise ValueError

        if start_date >= end_date:
            print('end_date must be after start_date')
            raise er.EndDateBeforeStartDate

        if site_scrapy not in self._list_sites_scrapy:
            print('site_scrapy must be a str and be one of these values')
            print(self._list_sites_scrapy)
            raise er.NotinList

        if size not in self._list_sizes_alphavantage:
            print('size must be a str and be one of these values')
            print(self._list_sizes_alphavantage)
            raise er.NotinList

        if not isinstance(key_path, str):
            print('key_path should be a str with path of key directory')
            raise ValueError

        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.site_scrapy = site_scrapy
        self.timeframe = timeframe
        self.size = size
        self.key_path = key_path

        if self.site_scrapy == 'yfinance':
            self.dataframe = self.get_yfinance_data()

        if self.site_scrapy == 'alphavantage':
            self.dataframe = self.get_alphavantage_data()

    def get_yfinance_data(self):
        dataframe = yf.download(ticker, td_start, td_end, interval=st_interval)

    def get_alphavantage_data(self):
        pass
