from io import BytesIO
import holoviews as hv
import pandas as pd
import panel as pn


#load data
@pn.cache
def get_stocks(data):
    if data is None:
        stock_file = 'https://datasets.holoviz.org/stocks/v1/stocks.csv'
    else:
        stock_file = BytesIO(data)
    return pd.read_csv(stock_file, index_col='Date', parse_dates=True)



