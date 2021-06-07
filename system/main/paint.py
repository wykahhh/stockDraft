import tushare as ts
import mplfinance as mpf
import os,sys
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tushare.stock.trading import get_hist_data
from matplotlib import ticker
from matplotlib.pylab import date2num
import numpy as np

token='3b3eb46262e0ed413eb529f63de45817416cbef5932da6131f285507'
pro=ts.pro_api(token)

def paint(code,end):
    daily=pro.daily(ts_code=code,start_date='20200601',end_date=end)
    daily.index=daily.trade_date
    daily=daily.rename(index=pd.Timestamp)
    daily.drop(columns=['ts_code','trade_date','pre_close','change','pct_chg','amount'],inplace=True)
    daily.columns=['open','high','low','close','volume']
    daily.sort_index(inplace=True)
    mpf.plot(daily,type='candle',volume=True,style='yahoo',mav=(5,10,20,30),datetime_format="%Y-%m-%d",savefig=f"./media/{code}.png")
