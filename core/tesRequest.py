#!/usr/bin/python#
# -*- coding: UTF-8 -*-
# 基础包：接口测试的封装

import xmltodict
import requests
import json
from requests.auth import *

import tesLog as log

logging = log.getLogger()


def api_test(method, url, data, headers, assertKey, **kwargs):
    """
    定义一个请求接口的方法和需要的参数
    :Args:
    method  - 接口方法名称 str
    url - 接口路径 str
    data - 参数 str
    headers - 请求头信息 dict
    非RESTful API请求另外的请求类型实际用不到。也不安全。
    """
    logging.info('URL: %s ', url)
    logging.info('Request: %s ', str(data))
    try:
        if method == "post":
            results = requests.post(url, data, headers=headers, verify=False)
        if method == "post-d":
            results = requests.post(url, data, headers=headers, auth=HTTPDigestAuth(kwargs['digestusername'],
                                                                                      kwargs['digestpassword']))
        if method == "get":
            results = requests.get(url, data, headers=headers)
        if method == "get-d":
            results = requests.get(url, data, headers=headers, auth=HTTPDigestAuth(kwargs['digestusername'],kwargs['digestpassword']))
        if method == "put":
            results = requests.put(url, data, headers=headers)
        if method == "delete":
            results = requests.delete(url, headers=headers)
        if method == "patch":
            results == requests.patch(url, data, headers=headers)
        if method == "options":
            results == requests.options(url, headers=headers)
        if results is not None:
            try:
                responsetxt = results.text
                jsonresponse = results.text
                if "<?xml" in jsonresponse:
                    jsonresponse = json.dumps(dict(xmltodict.parse(jsonresponse)))
            except Exception as e:
                logging.error("response 解析异常:%s", e)
                return 'RequestIsERROR', '-1'
        else:
            return 'RequestIsERROR', '-1'

        """开始取检查字段的值"""
        actualCode = ""
        i = 0
        assertKeyList = assertKey.split("|")
        for key in assertKeyList:
            code = json.loads(jsonresponse)
            keyList = key.split(".")
            for k in keyList:
                if k.find("#") > 0:
                    s = k.split("#")
                    code = code[s[0]]
                    for l in range(1,len(s)):
                        code = code[int(s[l])]
                else:
                    code = code[k]
            if i < 1:
                actualCode += str(code)
            else:
                actualCode = actualCode + "|" + str(code)
            i += 1

        logging.info("Response: %s", responsetxt)
        results.close()
        return jsonresponse, actualCode
    except Exception, e:
        logging.error("Service is error %s", e)
        logging.error("Service return response :" + str(responsetxt))
        return 'RequestIsERROR', '-1'

