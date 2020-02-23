# -*- coding:utf-8 -*-
#coding=utf-8
import sys

import maintest


def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs


def count2():
    fs = []

    def f(j):
        def g():
            return j * j
        return g

    for i in range(1,4):
        fs.append(f(i))

    return fs


def log(func):
    def wrapper(*args,**kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper()

@log
def now():
    print("this is now :2019")

now