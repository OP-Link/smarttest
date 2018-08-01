#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

import oprsrc.common as common
import core.tesLog as log
import core.tesReport as report
import gl

# 验证包：接口测试脚本
logging = log.getLogger ( )

"""1.外部输入参数"""
path = sys.path[0]  # 当前路径
product = sys.argv[1]  # 项目名称
module = sys.argv[2]  # 服务模块名
version = sys.argv[3]    # 版本
platform = sys.argv[4]    # 平台环境
url = sys.argv[5]       # 服务地址
dbhost = sys.argv[6]      # 数据库地址
user = sys.argv[7]      # 数据库用户名
password = sys.argv[8]   # 数据库密码
dbname = sys.argv[9]        # 数据库名称

gl._init()
gl.set_value("dbhost", dbhost)
gl.set_value("user", user)
gl.set_value("password", password)
gl.set_value("dbname", dbname)
testInfo = report.get_test_info ( test_name=product + "-" + module, test_version=version, test_pl=platform,
                                  test_net=url )


"""2.根据module获取Sheet"""
logging.info ( "-------------- Execute TestCases ---------------" )
sheet = common.get_excel_sheet ( path + "/testCase/" + product + ".xlsx", module )

"""3.数据准备"""
logging.info ( "-------------- Prepare Data Through MysqlDB --------------" )
sql = common.get_prepare_sql ( sheet )
common.prepare_data ( host=dbhost, user=user, password=password, db=dbname, sql=sql )

"""4.执行测试用例,获取执行结果"""
logging.info ( "-------------- Execute Test Cases --------------" )
testSumInfo, testDetailInfo = common.run_test ( sheet, product + "-" + module, url )

"""5.生成测试报告"""
logging.info ( "-------------- Create The ReportExcel ------------" )
report.creat_report_excel (gl.logpath(), module, testInfo, testSumInfo, testDetailInfo )

"""6.数据清理"""
logging.info ( "-------------- Delete Data From MysqlDB --------------" )
del_sql = common.get_prepare_del_sql ( sheet )
common.prepare_data ( host=dbhost, user=user, password=password, db=dbname, sql=del_sql )
logging.info ( "-------------- The End ------------" )