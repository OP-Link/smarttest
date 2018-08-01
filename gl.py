#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 脚本功能：全部变量

import time
import uuid
import platform

CASE_NUMBER = 0  # 用例编号
CASE_NAME = 1    # 用例名称
IS_RUN_SWITCH = 2  # 是否执行开关列数  N 为不执行，其他为执行
CASE_DATA = 3    # 用例参数
CASE_URL = 4     # 用例接口地址
CASE_METHOD = 5  # 用例请求类型
CASE_Digest = 6
CASE_HEADERS = 7  # 用例headers
CASE_KEY = 8    # 判断key
CASE_CODE = 9    # 判断value
DATA_TO_STORE = 10  # 需要保存response中的key
DATA_TO_REPLACE = 11   # 参数化条件
PRE_SQL = 12           # 该行用例执行前需要执行的sql


SQL_ROW = 0      # 预执行SQL的行号
SQL_COL = 0      # 预执行SQL的列号

DEL_ROW = 0      # 执行后清理数据SQL的行号
DEL_COL = 1      # 执行后清理数据SQL的列号
# FILE_NAME = 'test_hoa.xlsx'
PLACE_HOLDER = ''


def logpath():
    sysstr = platform.system()
    if (sysstr == "Windows"):
        return './reports/'
    elif (sysstr == "Linux"):
        return '/opt/report_log/'

def _init():
    global _global_dict
    _global_dict = {}
def set_value(name, value):
    _global_dict[name] = value
def get_value(name, default=None):
    try:
        return _global_dict[name]
    except KeyError:
        return default
