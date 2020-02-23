# -*- coding:utf-8 -*-
#coding=utf-8
import tushare as ts
import os

print(ts.__version__)
#参数 示例 '600848',start='2015-01-05',end='2015-01-09'
#
#
def downloadData(code,starttime='',endtime=''):
    if starttime.strip()=='' and endtime.strip()=='':
        df_data_60 = ts.get_hist_data(code,ktype='60')[0:60]
    else:
        df_data_60 = ts.get_hist_data(code=code,start=starttime,end=endtime,ktype='60')[0:60]

    df_data_60 = df_data_60.sort_values(by=['date'])
    print(df_data_60)
    print("**")
    filename = "standard_60.csv"
    if os.path.isfile(filename):
        os.remove(filename)

    df_data_60.to_csv(filename,mode='a',header=None)

downloadData('600848')