# -*- coding:utf-8 -*-
#coding=utf-8

import tushare as ts
import time
import pandas as pd
import json
from sql_util import SQL_OP

def record_db(code):
    db = SQL_OP()
    db.search("select * from df_50 where code = '%s'" % str(code))


def record_Info(code_list):
    db = SQL_OP()
    data_dict = {"data":[]}
    if len(code_list):
        for code in code_list:
            df_h = ts.get_hist_data(code).head(1)
            open_price = df_h['open'][0]
            high_price = df_h['high'][0]
            close_price = df_h['close'][0]
            low_price = df_h['low'][0]
            open_close_rate = (close_price - open_price) / open_price
            low_high_rate = (high_price - low_price) / low_price
            strtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            stock_info = {"date": strtime, "code": code, "open_price": open_price, "close_price": close_price,
                          "low_price": low_price, "high_price": high_price, "open_close_rate": open_close_rate,
                          "low_high_rate": low_high_rate}
            data_dict["data"].append(stock_info)
            # record to database
            #record_to_db(code)
            db.record_to_db(code)

    return data_dict
