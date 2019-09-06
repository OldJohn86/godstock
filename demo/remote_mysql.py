# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
from datetime import date

import pymysql
# 指定过滤告警的类别为 pymysql.Warning类
from warnings import filterwarnings
# 动作为"error",该动作可以抛错，则可以用try ... except 捕获
#filterwarnings("error",category=pymysql.Warning)
# 动作为"ignore", 表示忽略
filterwarnings("ignore",category=pymysql.Warning)

import tushare as ts
#自定义的module
import cfg

# 数据库类定义
class MysqlDB():
    def __init__(self, host='localhost', port=3306, db='', user='', passwd='root', charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cursor = self.conn.cursor() # cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self
    
    def version(self):
        # 使用execute()方法执行SQL查询
        self.cursor.execute("SELECT VERSION()")
        # 使用fetchone() 方法获取单条数据
        data = self.cursor.fetchone()
        # 打印数据库版本信息
        print("Database version ：%s " % data)

    def create_table(self, table):
        self.cursor.execute('DROP TABLE IF EXISTS %s' % table)
        sql = """CREATE TABLE EMPLOYEE (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,
                 SEX CHAR(1),
                 INCOME FLOAT)"""
        self.cursor.execute(sql)

    def insert(self, item):
        #sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
        #         LAST_NAME, AGE, SEX, INCOME)
        #         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
               LAST_NAME, AGE, SEX, INCOME) \
               VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
               ('Mac', 'Mohan', 20, 'M', 2000)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
    
    def query(self):
        #sql = "SELECT * FROM EMPLOYEE \
        #       WHERE INCOME > %s" % (1000)
        sql = "SELECT * FROM daily_600519 where close > 1000"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = db.cursor.fetchall()
            for row in results:
                # 打印结果
                print ("ts_code=%s \ttrade_date=%s \tclose=%s \tvol=%s \tamount=%s" % \
                        (row[1], row[2], row[6], row[10], row[11]))
        except:
            print ("Error: unable to fetch data")

    def update(self):
        sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()

    def delete(self):
        sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()


if __name__ == '__main__':
    current_path = sys.argv[0].rstrip('/remote_mysql.py')
    # print(current_path)
    config = os.path.join(current_path, '../ts_config.ini')
    # print(config)

    mysql_info = cfg.read_ini(config, 'mysql')
    host = str(mysql_info.get('host', None))
    # print(host)
    user = str(mysql_info.get('user', None))
    # print(user)
    passwd = str(mysql_info.get('passwd', None))
    # print(passwd)
    database = str(mysql_info.get('database', None))
    # print(database)

    with MysqlDB(host=host, user=user, passwd=passwd, db=database) as db:
        #1 获取DB版本信息
        db.version()
        #2 创建数据库表
        # db.create_table('EMPLOYEE')
        #3 SQL 插入语句
        # db.insert('sss')
        #4 SQL 查询语句
        db.query()
        #5 SQL 更新语句
        # db.update()
        # db.query()
        #6 SQL 删除语句
        #db.delete()
