# -*- coding:utf-8 -*-
#coding=utf-8

import  tushare as ts
import numpy as np
import math
import matplotlib.pyplot as plt

def mean(x):
    return sum(x)/len(x)
# 计算每一项数据与均值的差
def de_mean(x):
  x_bar = mean(x)
  return [x_i - x_bar for x_i in x]
# 辅助计算函数 dot product 、sum_of_squares
def dot(v, w):
  return sum(v_i * w_i for v_i, w_i in zip(v, w))
def sum_of_squares(v):
  return dot(v, v)
# 方差
def variance(x):
  n = len(x)
  deviations = de_mean(x)
  return sum_of_squares(deviations) / (n - 1)
# 标准差
def standard_deviation(x):
  return math.sqrt(variance(x))
# 标准差
def standard_deviation(x):
  return math.sqrt(variance(x))

def covariance(x, y):
  n = len(x)
  return dot(de_mean(x), de_mean(y)) / (n -1)
# 相关系数
def correlation(x, y):
  stdev_x = standard_deviation(x)
  stdev_y = standard_deviation(y)
  if stdev_x > 0 and stdev_y > 0:
    return covariance(x, y) / stdev_x / stdev_y
  else:
    return 0

#统一计量 格式化数据
def formatData(vals_code):
  code_max = vals_code.max()
  if code_max<1:
    return vals_code
  else:
    c = 0
    while code_max>10:
      code_max=code_max//10
      c = c+1
    sq = (int(code_max)+1)*(10**c)
    vals_code = vals_code/sq
    return vals_code

# 图形化展示
def display(vals_code,vals_sample,code):
  t = np.arange(len(vals_code))
  vals_sample = formatData(vals_sample)
  vals_code = formatData(vals_code)
  # print(vals_sample)
  # print(vals_code)
  plt.plot(t, vals_sample, lw=1.0)  # lw 代表线条粗细
  plt.plot(t, vals_code, lw=2.0)
  plt.title(code)
  plt.show()
  return

#判断相关系数
#指定code 股票
#sampleDir 指定模型样本数据
#flag 要求达到的最小相关系数
#
def corrIndex(code,sampleDir,flag):
  #读取sample数据
  resCorr = -1
  try:
    df_60 = ts.get_hist_data(code, ktype='60')[0:60]  #获取60分钟k线数据
  except Exception:
    return -1
  #print(df_60)
  #空数据直接返回
  if df_60.empty:
    return -1
  df_60 = df_60.sort_values(by=['date'])
  data_60 = np.array(df_60['close'])
  #第四列数据是close价格
  sample_60 = np.loadtxt(sampleDir, delimiter=',', usecols=(3,), unpack=True)

  t = np.arange(len(data_60))  # 数组
  poly_data = np.polyfit(t, data_60, 15)
  poly_sample = np.polyfit(t, sample_60[0:len(data_60)], 15)#会出现 data_60的长度和 data_sample不一致的情况

  #拟合数据
  vals_data = np.polyval(poly_data, t)
  vals_sample = np.polyval(poly_sample,t)
  # print(vals_data)
  # print(vals_sample)
  #
  resCorr = correlation(vals_data,vals_sample)
  #print(resCorr)
  if resCorr >flag:
    print(resCorr,code)
    display(vals_data, vals_sample,code)
    return resCorr

  return -1


#corrIndex('000002','myl_60_standard.csv')