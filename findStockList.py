# -*- coding:utf-8 -*-
#coding=utf-8

import tushare as ts
import pandas as pd
import numpy as np

import covIndex
import  MACD
import initData
import IsBetween
import time
import os
import json
import record_result

#性能定位
#import profile
import threading

lock = threading.Lock()
task_id = 0
resList = []

def getValCodeList(codelist,name):
  #codelist = codelist

  global lock
  global task_id
  global resList
  num_all = len(codelist)
  # for i in range(len(codelist)):
  #   if covIndex.corrIndex(codelist[i],'myl_60_standard.csv',0.94)!= -1:
  #       resList.append(codelist[i])

  #多线程
  while task_id < num_all:
    lock.acquire()
    try :
        if task_id < num_all:
            if covIndex.corrIndex(codelist[task_id], 'myl_60_standard.csv', 0.94) != -1:
                    print(name)
                    resList.append(codelist[task_id])
            task_id =task_id+1
    finally:
        lock.release()
  # print(resList)
  #
  # return resList

def mythread(codelist_all):
    thread_all=[]
    for i in range(8):
        thread_name = "thread num is "+str(i)
        t = threading.Thread(target=getValCodeList,args=(codelist_all,thread_name,))
        thread_all.append(t)
        t.start()
    for i in range(8):
        thread_all[i].join()


if __name__=="__main__":
    #global resList
    print("[+]-------FTW--------[+]")
    # 1 返回相关系数符合的列表

    codelist_all = initData.initCodelist('')
    #code_num = len(codelist_all)

    #codelist = getValCodeList(codelist_all)
    mythread(codelist_all)


    resListgood = []
    resListperfect = []
    print("valcodelist is :\n"+str(resList))
    starttime = time.time()
    for i in range(len(resList)):
        # 2 过滤 符合在20和60 日均线之间的列表
        if IsBetween.isBetween60and20(resList[i]):
            # 3 判断MACD 变化趋势和 峰值大小 返回符合列表
            strRes = MACD.MACDChoose(resList[i])
            if ('good' in strRes):
                print(strRes)
                resListgood.append(resList[i])
            elif 'perfect' in strRes:
                resListperfect.append(resList[i])
                print(strRes)

    print('good list is :' + str(resListgood))
    print('perfect list is :' + str(resListperfect))
    endtime = time.time()
    print(endtime-starttime)



    good_dict = record_result.record_Info(resListgood)
    perfect_dict = record_result.record_Info(resListperfect)
    strout = {'good list': [], 'perfect list': []}
    strout['good list'].append(good_dict)
    strout['perfect list'].append(perfect_dict)

    perdictfilename = time.strftime('%Y%m%d.txt', time.localtime(time.time()))
    if os.path.isfile('./perdictFiles/' + perdictfilename):
        os.remove('./perdictFiles/' + perdictfilename)
    f1 = open('./perdictFiles/' + perdictfilename, 'w')
    f1.writelines(strout)
    f1.flush()




