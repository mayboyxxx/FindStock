# -*- coding:utf-8 -*-
#coding=utf-8

import tushare as ts
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt



# 图形化展示
def display(vals_code,code):
  t = np.arange(len(vals_code))
  plt.plot(t, vals_code, lw=2.0)# lw 代表线条粗细
  plt.title(code)
  plt.show()
  return


code = 'sh600765'
df_60 = ts.get_h_data(code,start='2013-03-01', end='2013-03-14',autype='none') #获取60分钟k线数据
#df_60 = ts.get_hist_data(code, ktype='60')[0:60]  #获取60分钟k线数据
print(df_60)

df_60 = df_60.sort_values(by=['date'])
data_60 = np.array(df_60['close'])

t = np.arange(len(data_60))  # 数组
poly_data = np.polyfit(t, data_60, 15)

vals_data = np.polyval(poly_data, t)
display(vals_data,code)
