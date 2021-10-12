from backtesting_numba.download_data import DownloadData

data_yf = DownloadData('MSFT')
dataframe_yf = data_yf.dataframe.copy()

dataframe_yf.columns = [column.lower() for column in dataframe_yf.columns]

dataframe_yf.to_csv('../sample_data/MSFT.csv')
