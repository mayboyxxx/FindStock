# -*- coding:utf-8 -*-
#coding=utf-8

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
resList=['603889', '603663', '603618', '603588', '603283', '603179', '601990', '601866', '601616', '600888', '600798', '600686', '600677', '600624', '600593', '600510', '600495', '600485', '600295', '600247', '600137', '600110', '600095', '600078', '600052', '300654', '300648', '300440', '300429', '300150', '300138', '300112', '300090', '300067', '300057', '300022', '002742', '002735', '002685', '002602', '002512', '002502', '002390', '002348', '002339', '002321', '002225', '002221', '002160', '002105', '000982', '000925', '000778', '000756', '000712', '000669', '000631', '000616', '000536', '000415', '000150', '000035', '000011', '600485', '600247']
resListgood = []
resListperfect = []
task_id=0
def getcodelist(code_list,name):
    global resListgood
    global resListperfect
    global task_id
    #print("valcodelist is :\n" + str(resList))
    list_len = len(resList)
    while task_id < list_len:
        lock.acquire()
        try:
            # 2 过滤 符合在20和60 日均线之间的列表
            if task_id < list_len:
                print("taskid is :"+str(task_id)+" threading num "+name)
                if IsBetween.isBetween60and20(resList[task_id]):
                # 3 判断MACD 变化趋势和 峰值大小 返回符合列表
                    strRes = MACD.MACDChoose(resList[task_id])
                    if ('good' in strRes):
                        print(strRes)
                        resListgood.append(resList[task_id])
                    elif 'perfect' in strRes:
                        resListperfect.append(resList[task_id])
                        print(strRes)
            task_id = task_id+1
        finally:
            lock.release()



def mythread(codelist_all):
    thread_all=[]
    for i in range(8):
        thread_name = "thread num is "+str(i)
        t = threading.Thread(target=getcodelist,args=(codelist_all,thread_name,))
        t.start()
        thread_all.append(t)
        print("thread "+str(i)+" is running")
    for i in range(8):
        thread_all[i].join()


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 10)
        # 释放锁
        threadLock.release()


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
        print(counter)


threadLock = threading.Lock()
threads = []



if __name__ == "__main__":
    print(len(resList))
    starttime = time.time()
   # mythread(resList)

    # t1 = threading.Thread(target=getcodelist,args=(resList,"thread1",))
    # t2 = threading.Thread(target=getcodelist,args=(resList,"thread2",))
    # t3 = threading.Thread(target=getcodelist,args=(resList,"thread3",))
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()

    endtime = time.time()
    print(endtime - starttime)
    print("resListgood is :" +str(resListgood))
    print("resListperfect is :"+str(resListperfect))

    # 创建新线程
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)

    # 开启新线程
    thread1.start()
    thread2.start()

    # 添加线程到线程列表
    threads.append(thread1)
    threads.append(thread2)

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")

