# -*- coding:utf-8 -*-
#coding=utf-8
# -*- coding:utf-8 -*-
#coding=utf-8
import sys

import json
import pandas as pd
import tushare as ts
import numpy as np
import datetime
import time
#获取数据
#df=pd.read_csv('C:/Users/HXWD/Desktop/000001.csv',encoding='gbk')

def get_EMA(df,N):
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'close']
        if i>0:
            df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)
    ema=list(df['ema'])
    return ema
def get_MACD(df,short=12,long=26,M=9):
    a=get_EMA(df,short)
    #print(pd.Series(a))
    b=get_EMA(df,long)
    #print(pd.Series(b))
    #print(pd.Series(a)-pd.Series(b))
    #df['diff'] = pd.Series(a) - pd.Series(b)
    # df['diff'] = None
    # print("test----")
    # print(df)

    for i in range(len(df)):
        df.ix[i,'diff']=a[i]-b[i]
        if i==0:
            df.ix[i,'dea']=df.ix[i,'diff']
        if i>0:
            df.ix[i,'dea']=(2*df.ix[i,'diff']+(M-1)*df.ix[i-1,'dea'])/(M+1)
    df['macd']=2*(df['diff']-df['dea'])
    return df

#print(df)


def initData(code):
    df = ts.get_hist_data(code,ktype='30')
    # df.columns=[u'open', u'high', u'close', u'low', u'volume', u'price_change',u'p_change', u'ma5', u'ma10', u'ma20', u'v_ma5', u'v_ma10', u'v_ma20',u'turnover']
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df = df.sort_values(by='date', axis=0, ascending=True)
    df = get_MACD(df, 12, 26, 9)
    df = df.sort_values(by='date', axis=0, ascending=False)[0:60]
    #print(df)
    return df

def getAreaAndBiggest(df,start,li):
    resArray =[]
    for i in range(len(li)):
        if i==0:#第一个节点
            area = 0
            biggest=0
            for j in range(start,li[i]+1):
                if abs(df.ix[j,'macd'])>biggest:
                    biggest=abs(df.ix[j,'macd'])
                area = area+df.ix[j,'macd']
            #jsonNode = '{"id":%d,"area":%.6f,"biggest":%.6f}' % (i,area,biggest)
            #jsonData = json.loads(jsonNode)
            jsonNode = {"id": 0, "area": 0, "biggest": 0}
            jsonNode["id"] = i
            jsonNode["area"] = area
            jsonNode["biggest"] = biggest
            resArray.append(jsonNode)
        else:#第i个节点
            area = 0
            for j in range(li[i-1]+1,li[i]+1):
                if abs(df.ix[j,'macd'])>biggest:
                    biggest=abs(df.ix[j,'macd'])
                area = area+df.ix[j,'macd']
            #jsonNode ={}
            # jsonData = json.loads(jsonNode)
            jsonNode = {"id":0,"area":0,"biggest":0}
            jsonNode["id"]=i
            jsonNode["area"]=area
            jsonNode["biggest"]=biggest
            resArray.append(jsonNode)
    #print(resArray)
    return resArray

def calcTrend(df_input):
    df_input = df_input[0:60]
    li =[] # 用于存储符号变化的分界点
    index =0
    while df_input.ix[index,'macd']>0:
        index =index+1
    #print(df_input)
    #print(index)
    for i in range(index,len(df_input)):
        if df_input.ix[i,'macd']<0 and i<len(df_input)-1 and df_input.ix[i+1,'macd']>0 :
            #print(i)
            li.append(i)
        elif df_input.ix[i,'macd']>0 and i<len(df_input)-1 and df_input.ix[i+1,'macd']<0:
            #print(i)
            li.append(i)
    #print(len(li))
    #return li
    #print(li)
    resArray = getAreaAndBiggest(df_input,index,li)
    return resArray


def MACDChoose(code):
    resArray = calcTrend(initData(code))
    #resArray = calcTrend(initData("000002"))
    #for i in range(0,len(resArray)):
    #print(resArray)
    if len(resArray)>=5:
        if abs(resArray[0]['area'])<=abs(resArray[2]['area']) and abs(resArray[2]['area'])<=abs(resArray[4]['area']) and resArray[0]['biggest']<=resArray[2]['biggest'] and resArray[0]['biggest']<=resArray[2]['biggest']:
            restr = "perfect code is "+str(code)
            return restr
    elif len(resArray)>=3:
        if abs(resArray[0]['area'])<=abs(resArray[2]['area'])  and resArray[0]['biggest']<=resArray[2]['biggest']:
            restr = "good code is " + str(code)
            return restr

    return "bad"
