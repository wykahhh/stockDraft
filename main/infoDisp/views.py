from django.shortcuts import render
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
# Create your views here.

def Disp(request):
    if request=="POST":
        