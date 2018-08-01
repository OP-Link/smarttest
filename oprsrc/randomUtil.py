#coding:utf-8

import random
import time
import datetime

"""
产生随机参数，待需求确认需要哪些随机数据
"""


def randomUid():
    pass


def randomEmail():
    pass


def time_now():
    """返回当前时间"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def time_today():
    """返回今天的00:00:00点"""
    return time.strftime("%Y-%m-%d 00:00:00", time.localtime())


def time_future():
    """返回30天后的00:00:00点"""
    day = datetime.datetime.now()
    date = day + datetime.timedelta(days=30)
    return str(date)[0:10] + " 00:00:00"


def time_next_month():
    """返回次月1日凌晨00:00:00"""
    day_tuple = time.localtime()
    day_list = list(day_tuple)
    if day_list[1] == 12:
        day_list[0] += 1
        day_list[1] = 1
        day_list[2] = 1
    else:
        day_list[1] += 1
        day_list[2] = 1
    return time.strftime("%Y-%m-%d 00:00:00",tuple(day_list))


def date_today():
    """返回当前日期"""
    return time.strftime("%Y-%m-%d", time.localtime())


def date_next_month():
    """返回次月1号的日期"""
    day_tuple = time.localtime()
    day_list = list(day_tuple)
    if day_list[1] == 12:
        day_list[0] += 1
        day_list[1] = 1
        day_list[2] = 1
    else:
        day_list[1] += 1
        day_list[2] = 1
    return time.strftime("%Y-%m-%d", tuple(day_list))

def date_month_later():
    """返回30天后的日期"""
    day = datetime.datetime.now()
    date = day + datetime.timedelta(days=30)
    return str(date)[0:10]

print time_next_month()
print date_next_month()