import os
from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import time
from plotly.graph_objs import *
from plotly import tools
from plotly.offline import init_notebook_mode, iplot, iplot_mpl

# Initialize Binance client
api_key = os.getenv("CLIENT_KEY")
api_secret = os.getenv("SECRET_KEY")
client = Client(api_key, api_secret)

class BinanceClient(Client):
  def __init__(self):
    api_key = os.getenv("CLIENT_KEY")
    api_secret = os.getenv("SECRET_KEY")
    self.client = Client(api_key, api_secret)

    # Format klines to dataframe
    _columns=[
      'Open time',
      'Open',
      'High',
      'Low',
      'Close',
      'Volume',
      'Close time',
      'Quote asset volume',
      'Number of trades',
      'Taker buy base asset volume',
      'Taker buy quote asset volume',
      'ignore'
    ]

  def get_price_data_1mo_1day(self):
    # alltime price data
    klines = self.client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "July 4, 2013 PST")
    return pd.DataFrame(klines, columns=self._columns).astype(float)

  def get_last_hour_price_data(self):
    klines = self.client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 hours ago UTC")
    return pd.DataFrame(klines, columns=self._columns).astype(float)
    

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "July 4, 2013 PST")
prices = pd.DataFrame(klines, columns=_columns).astype(float)

# Change timestamp to datetime
prices['Open time'] = prices['Open time'].apply(lambda x: dt.datetime.fromtimestamp(int(x)/1000))
prices = prices.set_index('Open time')
# Save data
prices.to_csv('btcusd.csv')

# Display data
plt.plot(prices['Close'])
plt.show()