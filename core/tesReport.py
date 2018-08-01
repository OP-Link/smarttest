# -*- coding: utf-8 -*-
import sys
import time

import xlsxwriter

reload(sys)
sys.setdefaultencoding("utf-8")


def get_test_info(test_name, test_version, test_pl, test_net):
    """获取测试信息"""
    test_info = {"test_name": test_name, "test_version": test_version, "test_pl": test_pl, "test_net": test_net}
    return test_info


def get_test_suminfo(test_sum, test_success, test_failed):
    """获取测试执行数量信息"""
    test_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    test_sum = {"test_sum": test_sum, "test_success": test_success, "test_failed": test_failed, "test_date": test_date}
    return test_sum


def get_test_detail(t_id, t_name, t_method, t_url, t_param,t_response, t_hope, t_actual, t_result):
    """获取执行的详细信息"""
    """
    t_id：用例编号
    t_name：用例名称
    t_method：接口方法
    t_url：接口地址
    t_param：接口报文
    t_response:接口返回
    t_hope：期望结果
    t_actual：实际结果
    t_result：执行结果 true false
    """
    test_detail = {"t_id": t_id, "t_name": t_name, "t_method": t_method, "t_url": t_url,
                   "t_param": t_param,"t_response":t_response,
                   "t_hope": t_hope, "t_actual": t_actual, "t_result": t_result}
    return test_detail


def get_all_test_detail(detaillist):
    detailData = {"info": detaillist}
    return detailData


def get_format(wd, option={}):
    return wd.add_format(option)


# 设置居中
def get_format_center(wd, num=1):
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})


def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)


# 写数据
def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))


def init(workbook, worksheet, testinfo, testsuminfo):
    # 设置列行的宽高
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 20)
    worksheet.set_column("E:E", 20)
    worksheet.set_column("F:F", 20)

    worksheet.set_row(1, 30)
    worksheet.set_row(2, 30)
    worksheet.set_row(3, 30)
    worksheet.set_row(4, 30)
    worksheet.set_row(5, 30)

    # worksheet.set_row(0, 200)

    define_format_H1 = get_format(workbook, {'bold': True, 'font_size': 18})
    define_format_H2 = get_format(workbook, {'bold': True, 'font_size': 14})
    define_format_H1.set_border(1)

    define_format_H2.set_border(1)
    define_format_H1.set_align("center")
    define_format_H2.set_align("center")
    define_format_H2.set_bg_color("blue")
    define_format_H2.set_color("#ffffff")
    # Create a new Chart object.

    worksheet.merge_range('A1:F1', '测试报告总概况', define_format_H1)
    worksheet.merge_range('A2:F2', '测试概括', define_format_H2)
    worksheet.merge_range('A3:A6', '这里放图片', get_format_center(workbook))

    _write_center(worksheet, "B3", '项目名称', workbook)
    _write_center(worksheet, "B4", '版    本', workbook)
    _write_center(worksheet, "B5", '平台环境', workbook)
    _write_center(worksheet, "B6", '地    址', workbook)

    # data = {"test_name": "智商", "test_version": "v2.0.8", "test_pl": "android", "test_net": "wifi"}
    _write_center(worksheet, "C3", testinfo['test_name'], workbook)
    _write_center(worksheet, "C4", testinfo['test_version'], workbook)
    _write_center(worksheet, "C5", testinfo['test_pl'], workbook)
    _write_center(worksheet, "C6", testinfo['test_net'], workbook)

    _write_center(worksheet, "D3", "接口总数", workbook)
    _write_center(worksheet, "D4", "通    过", workbook)
    _write_center(worksheet, "D5", "失    败", workbook)
    _write_center(worksheet, "D6", "测试日期", workbook)

    # data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
    _write_center(worksheet, "E3", testsuminfo['test_sum'], workbook)
    _write_center(worksheet, "E4", testsuminfo['test_success'], workbook)
    _write_center(worksheet, "E5", testsuminfo['test_failed'], workbook)
    _write_center(worksheet, "E6", testsuminfo['test_date'], workbook)

    _write_center(worksheet, "F3", "分数", workbook)

    worksheet.merge_range('F4:F6', round(100 * testsuminfo['test_success'] / testsuminfo['test_sum'], 2),
                          get_format_center(workbook))

    pie(workbook, worksheet)

    # 生成饼形图


def pie(workbook, worksheet):
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
        'name': '接口测试统计',
        'categories': '=测试总况!$D$4:$D$5',
        'values': '=测试总况!$E$4:$E$5',
    })
    chart1.set_title({'name': '接口测试统计'})
    chart1.set_style(10)
    worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


def test_detail(workbook, worksheet, testdetailinfo):
    # 设置列行的宽高
    worksheet.set_column("A:A", 20)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 20)
    worksheet.set_column("E:E", 20)
    worksheet.set_column("F:F", 20)
    worksheet.set_column("G:G", 20)
    worksheet.set_column("H:H", 20)

    worksheet.set_row(1, 30)
    # worksheet.set_row(2, 30)
    # worksheet.set_row(3, 30)
    # worksheet.set_row(4, 30)
    # worksheet.set_row(5, 30)
    # worksheet.set_row(6, 30)
    # worksheet.set_row(7, 30)


    worksheet.merge_range('A1:I1', '测试详情', get_format(workbook, {'bold': True, 'font_size': 18, 'align': 'center',
                                                                 'valign': 'vcenter', 'bg_color': 'blue',
                                                                 'font_color': '#ffffff'}))
    _write_center(worksheet, "A2", '用例ID', workbook)
    _write_center(worksheet, "B2", '接口名称', workbook)
    _write_center(worksheet, "C2", '接口协议', workbook)
    _write_center(worksheet, "D2", 'URL', workbook)
    _write_center(worksheet, "E2", '请求报文', workbook)
    _write_center(worksheet, "F2", '返回报文', workbook)
    _write_center(worksheet, "G2", '预期值', workbook)
    _write_center(worksheet, "H2", '实际值', workbook)
    _write_center(worksheet, "I2", '测试结果', workbook)

    temp = 3
    for item in testdetailinfo["info"]:
        worksheet.set_row(temp-1, 30)
        _write_center(worksheet, "A" + str(temp), item["t_id"], workbook)
        _write_center(worksheet, "B" + str(temp), item["t_name"], workbook)
        _write_center(worksheet, "C" + str(temp), item["t_method"], workbook)
        _write_center(worksheet, "D" + str(temp), item["t_url"], workbook)
        _write_center(worksheet, "E" + str(temp), item["t_param"], workbook)
        _write_center(worksheet, "F" + str(temp), item["t_response"], workbook)
        _write_center(worksheet, "G" + str(temp), item["t_hope"], workbook)
        _write_center(worksheet, "H" + str(temp), item["t_actual"], workbook)
        _write_center(worksheet, "I" + str(temp), item["t_result"], workbook)
        temp = temp + 1


def creat_report_excel(path, testmodel, testinfo, testsuminfo, testdetailinfo):
    workbook = xlsxwriter.Workbook(
        path + testmodel + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '-report.xlsx')
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")

    init(workbook, worksheet, testinfo, testsuminfo)
    test_detail(workbook, worksheet2, testdetailinfo)
    workbook.close()
