# !/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：excel的封装

import xlrd
workbook = None

def open_excel(path):
     """打开excel"""
     global workbook
     if (workbook == None):
          workbook = xlrd.open_workbook(path, on_demand=True)

def get_sheet(sheetName):
     """获取页名"""
     global workbook
     return workbook.sheet_by_name(sheetName)

def get_rows(sheet):
    """获取行号"""
    return sheet.nrows

def get_content(sheet, row, col):
    """获取表格中内容,解决Excel取值的一些格式问题"""
    ctype = sheet.cell ( row, col ).ctype  # 表格的数据类型
    cell = sheet.cell(row, col).value
    if ctype == 2 and cell % 1 == 0:  # 如果是整形
        cell = int ( cell )
    elif ctype == 3:
        # 转成datetime对象
        date = datetime ( *xldate_as_tuple ( cell, 0 ) )
        cell = date.strftime ( '%Y/%d/%m %H:%M:%S' )
    elif ctype == 4:
        cell = True if cell == 1 else False
    return cell

def release(path):
    """释放excel减少内存"""
    global workbook
    workbook.release_resources()
    del workbook
