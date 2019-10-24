#!/usr/env/bin python3
# -*- coding: utf-8 -*-

__author__ = 'Jonathan Chen'
__date__   = '2019-09-12'

import os
import sys
import time
import datetime
from datetime import date

import pymysql
from sqlalchemy import create_engine
# 指定过滤告警的类别为 pymysql.Warning类
from warnings import filterwarnings
# 动作为"error",该动作可以抛错，则可以用try ... except 捕获
#filterwarnings("error",category=pymysql.Warning)
# 动作为"ignore", 表示忽略
filterwarnings("ignore",category=pymysql.Warning)

import pandas as pd
# 自定义功能module
import cfg
import remote_mysql
import basic_data
import daily_data
import tick_data

stocklist = []
exchangelist = ['SSE', 'SZSE']
print(exchangelist)
'''
SSE  - 上交所
SZSE - 深交所
HKEX - 港交所（未上线)
'''
y_m_d = date.today().strftime('%Y%m%d')
print(y_m_d)

# basic opencal data
def sync_opencal_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%scal.xls" % (exchange, y_m_d))
            # print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'cal'),con=engine, \
                    if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err)

# company data
def sync_companylist_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%scompanylist.xls" % (exchange, y_m_d))
            # print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'companylist'),con=engine, \
                    if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err)

# basic stocklist data
def sync_stocklist_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%sstocklist.xls" % (exchange, y_m_d))
            # print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'stocklist'),con=engine, \
                    if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err)

# daily data
def sync_dailydata_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%sstocklist.xls" % (exchange, y_m_d))
            # print(df)
            for row in df.itertuples():
                #print(row.ts_code)
                stocklist.append(str(row.ts_code))
            # print(stocklist)
        except Exception as err:
            print(err)
    total = len(stocklist)
    msg = ''
    for i in range(len(stocklist)):
        try:
            df = pd.read_excel("backup/daily_%s.xls" % str(stocklist[i])[:-3])
            # print(df)
            df.to_sql(name=str('daily_'+ stocklist[i][:-3]),con=engine,if_exists='replace',index=False,index_label=False)
            print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' + str(stocklist[i]))
        except Exception as err:
            print(err)

def sync_all_to_sql(engine):
    # sync open cal to sql
    sync_opencal_to_sql(engine)
    # sync companylist to sql
    sync_companylist_to_sql(engine)
    # sync stocllist to sql
    sync_stocklist_to_sql(engine)
    # sync daily date to sql
    sync_dailydata_to_sql(engine)

def backup_all_to_excel(path):
    basic_data.main(path)


'''
    stock_info = cfg.read_ini(config, 'stock')
    stock_pool = str(stock_info.get('stock_pool', None)).split()
    # print(stock_pool)
'''
if __name__ == "__main__":
    cur_path = sys.argv[0].rstrip('/main.py')
    config = os.path.join(cur_path, '../ts_config.ini')
    #print(config)

    backup_all_to_excel(cur_path)

    mysql_info = cfg.read_ini(config, 'mysql')
    host = str(mysql_info.get('host', None))
    user = str(mysql_info.get('user', None))
    passwd = str(mysql_info.get('passwd', None))
    database = str(mysql_info.get('database', None))
    engine = create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % \
            (user, passwd, host, database))
    sync_all_to_sql(engine)

