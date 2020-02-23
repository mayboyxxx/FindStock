# -*- coding:utf-8 -*-
#coding=utf-8
import sys
import datetime
import tushare as ts


#判断区间D60 > price >D20   D60-price > price-D20
def isBetween60and20(code):
  endtime =datetime.datetime.now()
  starttime = endtime - datetime.timedelta(days=80)
  endtimestr = endtime.strftime("%Y-%m-%d")
  starttimestr = starttime.strftime("%Y-%m-%d")

  df_temp = ts.get_hist_data(code=code,start=starttimestr,end=endtimestr,ktype='60')
  #如果df数据为空 直接返回
  if df_temp.empty:
    return False
  #print(df_temp)
  current_price = float(df_temp[u'close'][0])
  # print("current_price is ====")
  # print(current_price)
  ma_20 = float(df_temp[u'ma20'][0])
  # print("ma_20 is ====")
  # print(ma_20)
  df_temp = df_temp.sort_values(by='date',axis=0,ascending=True)
  # print(df_temp)
  # print(df_temp[u'close'].rolling(60).mean().sort_index(ascending=False))
  ma_60=float(df_temp[u'close'].rolling(60).mean().sort_index(ascending=False)[0])
  # print("ma_60 is ====")
  # print(ma_60)

  if (ma_60>current_price) and (current_price>ma_20) and (ma_60+ma_20-2*current_price)>0:
    return True
  else:
    return False