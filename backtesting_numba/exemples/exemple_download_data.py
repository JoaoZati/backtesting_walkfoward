from backtesting_numba.download_data import DownloadData

data_yf = DownloadData('MSFT')
data_av = DownloadData('AAPL', site_scrapy='alphavantage', key_path='api_file.txt')

dataframe_yf = data_yf.dataframe.copy()
dataframe_av = data_av.dataframe.copy()

dataframe_yf.to_csv('../sample_data/MSFT.csv')
dataframe_av.to_csv('../sample_data/AAPL.csv')
