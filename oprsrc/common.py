#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 业务包：通用函数

import json
import xmltodict

import core.tesExcel as excel
import core.tesLog as log
import core.tesMysql as mysql
import core.tesReport as report
import core.tesRequest as request
import gl
import randomUtil


# filename = gl.FILE_NAME
logging = log.getLogger()
cachedResult = {}
global null , false , true
null = None
false = False
true = True


def prepare_data(host, user, password, db, sql):
    """数据准备，添加测试数据"""
    if len(sql) != 0:
        logging.info("RunSql:  %s", sql)
        db = mysql.create_engine(user, password, db, host)
        res = 0
        if sql.find(';') > 0:
            sqllist = sql.split(';')
            for sqll in sqllist:
                if len(sqll) > 1:
                    res += mysql.exc_sql(db, sqll)
        else:
            res = mysql.exc_sql(db, sql)
        logging.info("Run sql: the row number affected is %s", res)
        mysql.db_close(db)
        return res
    else:
        logging.info("No sql need to execute!")
        return


def get_excel_sheet(path, module):
    """依据模块名获取sheet"""
    excel.open_excel(path)
    return excel.get_sheet(module)


def replace_holder(value):
    """遍历字典替换占位符"""
    for holder in gl.PLACE_HOLDER:
        value = value.replace(holder, gl.PLACE_HOLDER[holder])
    return value


def get_prepare_sql(sheet):
    """获取预执行SQL"""
    return replace_holder(excel.get_content(sheet, gl.SQL_ROW, gl.SQL_COL))


def get_prepare_del_sql(sheet):
    """获取清理数据的SQL"""
    return replace_holder(excel.get_content(sheet, gl.DEL_ROW, gl.DEL_COL))


def pre_deal_testdata(testdata):
    """处理请求报文，替换请求报文中被参数化掉的参数"""
    data = str(testdata)
    if '$RANDOM' in data:
        data = data.replace("$RANDOMUID", randomUtil.randomUid()).replace("$RANDOMEMAIL", randomUtil.randomEmail())
    if '$TIME' in data:
        data = data.replace("$TIME_NOW", randomUtil.time_now()).replace("$TIME_TODAY", randomUtil.time_today()).replace("$TIME_FUTURE", randomUtil.time_future()).replace("$TIME_NEXT_MONTH", randomUtil.time_next_month())
    if '$DATE' in data:
        data = data.replace("$DATE_TODAY", randomUtil.date_today()).replace("$DATE_NEXT_MONTH", randomUtil.date_next_month()).replace("$DATE_MONTH_LATER", randomUtil.date_month_later())
    return data


def update_testdata_by_depend_case(testCase, resp, depend_detail):
    """根据依赖用例的返回结果，更新测试用例数据"""
    pass


def get_test_cases(sheet):
    """从excel获取用例，可以获取指定row的用例；默认获取所有需要执行的用例，返回testCase的dict"""
    testCases = []

    rows = excel.get_rows(sheet)
    for i in range(2, rows):
        """判断is_run_switch为N时，不需执行用例"""
        if str(excel.get_content(sheet, i, gl.IS_RUN_SWITCH)) == 'N':
            continue
        """获取所有需要执行的用例数据"""
        testCase = {}
        testCase["testNumber"] = str(excel.get_content(sheet, i, gl.CASE_NUMBER))
        if "</" in str(excel.get_content(sheet, i, gl.CASE_DATA)):
            tempData = json.dumps(dict(xmltodict.parse(str(excel.get_content(sheet, i, gl.CASE_DATA)))))
            testCase["testData"] = json.loads(tempData)
            testCase["isDataXml"] = 1
        else:
            testCase["testData"] = eval(pre_deal_testdata(excel.get_content(sheet, i, gl.CASE_DATA)))
            testCase["isDataXml"] = 0
        testCase["testName"] = excel.get_content(sheet, i, gl.CASE_NAME)
        testCase["testUrl"] = excel.get_content(sheet, i, gl.CASE_URL)
        testCase["testMethod"] = excel.get_content(sheet, i, gl.CASE_METHOD)
        testCase["testDigestInfo"] = excel.get_content(sheet, i, gl.CASE_Digest)
        testCase["testHeaders"] = str(excel.get_content(sheet, i, gl.CASE_HEADERS))
        testCase["testHeaders"] = eval(replace_holder(testCase["testHeaders"]))
        testCase["testAssertKey"] = excel.get_content(sheet, i, gl.CASE_KEY)
        testCase["testHopeCode"] = excel.get_content(sheet, i, gl.CASE_CODE)
        testCase["store"] = excel.get_content(sheet, i, gl.DATA_TO_STORE)
        testCase["replace"] = excel.get_content(sheet, i, gl.DATA_TO_REPLACE)
        testCase["pre_sql"] = excel.get_content(sheet, i, gl.PRE_SQL)
        testCases.append(testCase)

    return testCases


def excute_case(testCase, url):
    if testCase["isDataXml"] == 1:
        testCase["testData"] = xmltodict.unparse(testCase["testData"])
    else:
        testCase["testData"] = (json.dumps(testCase["testData"]))
    # 执行接口调用
    digestusername = None
    digestpassword = None
    if testCase["testDigestInfo"] is not None and testCase["testDigestInfo"] != "":
        if testCase["testDigestInfo"].find('|') > 0:
            """
            1、获取digest账号密码
            """
            digestinfo = testCase["testDigestInfo"].split('|')
            digestusername = digestinfo[0]
            digestpassword = digestinfo[1]
        testResponse, actualCode = request.api_test(testCase["testMethod"], url + testCase["testUrl"],
                                                    testCase["testData"], testCase["testHeaders"],
                                                    testCase["testAssertKey"],
                                                    digestusername=digestusername,
                                                    digestpassword=digestpassword)
        return testResponse, actualCode
    else:
        testResponse, actualCode = request.api_test(testCase["testMethod"], url + testCase["testUrl"],
                                                    testCase["testData"], testCase["testHeaders"],
                                                    testCase["testAssertKey"])
        return testResponse, actualCode


def store_data(keys, response, testCaseNumber):
    result = {}
    for k in keys.split("|"):
        temp = eval(response)
        for key in k.split("."):
            if key.find("#") > 0:
                s = key.split("#")
                temp = temp[s[0]]
                for l in range(1,len(s)):
                    temp = temp[int(s[l])]
            else:
                temp = temp[key]
        result[k] = temp
    cachedResult[str(testCaseNumber)] = result
    return cachedResult


def replace_data(testCase):
    condition_list = testCase["replace"].split("|")
    for con in condition_list:
        num = con.split(":")[0]
        key_list = con.split(":")[1].split(">")
        source_key = key_list[0]
        source = cachedResult[str(num)]
        dest_key = key_list[1]
        dest = testCase["testData"]
        for k in dest_key.split("."):
            if k.find("#") > 0:
                s = k.split("#")
                dest = dest[s[0]]
                for l in range(1,len(s)):
                    dest = dest[int(s[l])]
            else:
                dest = dest[k]
        temp = json.dumps(testCase["testData"])
        temp1 = temp.replace(str(dest), str(source[source_key]))
        testCase["testData"] = json.loads(temp1)


def run_test(sheet, module, url):
    """执行测试用例"""
    total_fail = 0
    testDetailList = []
    testCases = get_test_cases(sheet)
    tsum = len(testCases)

    for testCase in testCases:
        logging.info("Number %s", testCase["testNumber"])
        logging.info("CaseNmae %s", testCase["testName"])
        fail = 0
        #判断是否有sql需要先执行
        if testCase["pre_sql"] is not None and testCase["pre_sql"] != "":
            prepare_data(gl.get_value("dbhost"), gl.get_value("user"), gl.get_value("password"), gl.get_value("dbname"), str(testCase["pre_sql"]))
        # 判断是否需要替换参数化的testData
        if testCase["replace"] is not None and testCase["replace"] != "":
            replace_data(testCase)
        # 2.执行原用例
        testResponse, actualCode = excute_case(testCase, url)

        if testResponse is None:
            testResponse = 'response is null'

        # print str ( actualCode ), str ( expectCode )
        if actualCode is None or actualCode == 'RequestIsERROR':
            logging.error("Request is ERROR! %s", testCase["testNumber"])
            logging.info("----------Next Case----------")
            fail += 1
            total_fail += 1
        elif str(actualCode) != str(testCase["testHopeCode"]):
            logging.info("Fail: %s", testCase["testNumber"])
            logging.info("----------Next Case----------")
            fail += 1
            total_fail += 1
        else:
            # 用例执行成功后，判断是否需要存储response值
            if testCase["store"] is not None and testCase["store"] != "":
                store_data(testCase["store"], testResponse, testCase["testNumber"])

        if fail > 0:
            result = False
        else:
            logging.info("Pass: %s", testCase["testNumber"])
            logging.info("----------Next Case----------")
            result = True

        # 获取每次执行用例结果
        testDetail = report.get_test_detail(t_id=testCase["testNumber"], t_name=testCase["testName"],
                                            t_method=testCase["testMethod"], t_url=testCase["testUrl"],
                                            t_param=json.dumps(testCase["testData"]), t_response=testResponse,
                                            t_hope=testCase["testHopeCode"],
                                            t_actual=actualCode,
                                            t_result=result)
        testDetailList.append(testDetail)

    # 获取测试结果
    testSumInfo = report.get_test_suminfo(test_sum=tsum, test_success=tsum - total_fail, test_failed=total_fail)
    testDetailInfo = report.get_all_test_detail(testDetailList)

    return testSumInfo, testDetailInfo
