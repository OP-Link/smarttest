pychram破解  http://idea.lanyus.com/

pip install requests

pip install xlrd

pip install xlsxwriter

pip install mysql-connector-python

pip install xmltodict

A.下载mysql-connector-python-2.1.6-py2.7-winx64.msi，下载之后，根据提示安装即可.下载地址：https://dev.mysql.com/downloads/connector/python/




替换Lib目录下 site-packages / requests包里的 auth.py  （实现了和目digest鉴权、网关TR069鉴权、标准鉴权的分离）


——————runner 方法参数————————

ig cq_hoa V1.0.0 test http://172.19.1.203:8190 dbhost dbuser dbpwd dbname


testCase.xlsx中dataToStore和dataToReplace列填写示例：

dataToStore：该用例执行完后，需要保存response中某些值时，需要填写

            填写示例：devList#0.funtionList#0.openDate    字母代表字典的key，用“.”分离，数字代表列表的下标，用“#”分离;多个需要保存的值，用“|”分离 
            
dataToReplace:该用例执行前，需要用其他用例的执行结果，来参数化掉本用例的testData时，需要填写 

            填写示例：1-1:devList#0.funtionList#0.openDate>time   “:”前是该用例的用例编号(用例第一列的值)，“>”前是替换源，“>”后是替换目标，填写方式同dataToStore; 需要参数化多个值时用“|”分离。\n
            
pre_SQL列如果填写，会在执行该用例之前执行该SQL；
测试用例实践类参数化：
    在testData中，值设为 $TIME_NOW , $TIME_TODAY , $TIME_FUTURE ,会自动参数化为当前时间，当前日期0点，30天后的日期0点；
                 值设为  $DATE_TODAY, $DATE_NEXT_MONTH, $DATE_MONTH_LATER. 会自动参数化为 当前日期， 下月1号日期， 30天后的日期