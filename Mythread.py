# -*- coding:utf-8 -*-
#coding=utf-8

import time,threading,multiprocessing


class Mythread:

    def __init__(self,name):
        print('init')
        self.threadname = name
        self.lock = threading.Lock()

    def loop(self):
        x=0
    def add_to_list(self):
        pass

    def run_thread(self,code):
        #获取锁
        self.lock.acquire()
        try:
            #
            self.add_to_list()
        finally:
            #释放锁
            self.lock.release()
