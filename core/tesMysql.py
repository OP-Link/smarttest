# -*- coding: utf-8 -*-
import mysql.connector


# 打开数据库连接
def create_engine(user, password, db, host, port=3306):
    db = mysql.connector.connect(host=host,user=user,password=password,db=db,port=port)
    return db


# 使用cursor()方法获取操作游标
def exc_sql(db, sql):
    if db:
        cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return cursor.rowcount
    except Exception as ex:
        # Rollback in case there is any error
        db.rollback()
        return 0


def db_close(db):
    db.close()
