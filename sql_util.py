# -*- coding:utf-8 -*-
#coding=utf-8
import sys
from sqlalchemy import  create_engine
import pandas as pd
#import MySQLdb
import pymysql
import tushare as ts
import time
class SQL_OP:
    def __init__(self):
        try:
            self.db = pymysql.connect("localhost","root","","stock_database",charset='utf8')
            self.cursor = self.db.cursor()
        #print("1234")
        except:
            print("init db error ")

    def insert_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print(sql)
            print("insert error")
            #print("execute sql is : "+str(sql)+" error")

    def search(self,sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:

            print("execute sql is : "+str(sql)+" error")

    # engine =  create_engine('mysql+pymysql://root:qwer1234@localhost:3306/stock_database?charset=utf8')
    # df_50.to_sql('df50',engine,schema='stock_database',if_exists='append')
    # df_300.to_sql('df300',engine,schema='stock_database',if_exists='append')
    def record_to_db(self,code='',open_price='', close_price='', low_price='', high_price=''):
        db = SQL_OP()
        re = db.search("select * from finded_stock_list where code= '%s'" % (str(code)))
        # print(type(re))
        if open_price == '':
            df_h = ts.get_hist_data(code).head(1)
            open_price = df_h['open'][0]
            high_price = df_h['high'][0]
            close_price = df_h['close'][0]
            low_price = df_h['low'][0]
            print(type(open_price))

        if re:
            # 已经加入到观测
            print(re)
        else:
            # 未加入到观测
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            try:
                sql_insert = "insert into finded_stock_list (date,code,open_price,close_price,low_price,high_price,flag,rate_now) values ('%s','%s',%f,%f,%f,%f,%d,%f)" % (
                str(date), str(code), float(open_price), float(close_price), float(low_price), float(high_price), 0, 0.00)
                db.insert_data(sql_insert)
            except:

                print('record_to_db error')


    def destroy(self):
        try:
            self.db.close()
        except:
            print("db close error")



#db = SQL_OP()

#db.record_to_db('603486')

#db = SQL_OP()
#print(db.search("select * from df50"))
# print(type(db.search("select * from df50")))
