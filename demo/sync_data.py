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

'''
SSE  - 上交所
SZSE - 深交所
HKEX - 港交所（未上线)
'''
exchangelist = ['SSE', 'SZSE']
# print(exchangelist)
y_m_d = date.today().strftime('%Y%m%d')
# print(y_m_d)

'''
basic opencal data
'''
def sync_opencal_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%sopencal.xls" % (exchange, y_m_d))
#            print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'cal'), con=engine,
                    if_exists='replace', index=False, index_label=False)
            print('%s_%sopencal.xls has been sync to database!' % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
company data
'''
def sync_companylist_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%scompanylist.xls" % (exchange, y_m_d))
#            print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'companylist'), con=engine,
                    if_exists='replace', index=False, index_label=False)
            print('%s_%scompanylist.xls has been sync to database!' % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
basic stocklist data
'''
def sync_stocklist_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%sstocklist.xls" % (exchange, y_m_d))
#            print(df)
            df.to_sql(name=str(exchange.lower() +'_'+ y_m_d +'stocklist'), con=engine,
                    if_exists='replace', index=False, index_label=False)
            print('%s_%sstocklist.xls has been sync to database!' % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
daily data
'''
stocklist = []
def sync_dailydata_to_sql(engine):
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/%s_%sstocklist.xls" % (exchange, y_m_d))
#            print(df)
            for row in df.itertuples():
#                print(row.ts_code)
                stocklist.append(str(row.ts_code))
#            print(stocklist)
        except Exception as err:
            print(err)
#    print(stocklist)
    total = len(stocklist)
    msg = ''
    for i in range(len(stocklist)):
        try:
            df = pd.read_excel("backup/daily_%s.xls" % str(stocklist[i])[:-3])
#            print(df)
#            print(str('daily_'+stocklist[i][:-3]))
            df.to_sql(name=str('daily_'+ stocklist[i][:-3]), con=engine,
                    if_exists='replace', index=False, index_label=False)
            print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' +
                    str(stocklist[i]) + ' has been sync to database!')
        except Exception as err:
            print(err)

def main(path):
    config = os.path.join(path, '../ts_config.ini')
    print(config)
    mysql_info = cfg.read_ini(config, 'mysql')
    host = str(mysql_info.get('host', None))
    user = str(mysql_info.get('user', None))
    passwd = str(mysql_info.get('passwd', None))
    database = str(mysql_info.get('database', None))
    engine = create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % \
            (user, passwd, host, database))
    sync_opencal_to_sql(engine)
    sync_companylist_to_sql(engine)
    sync_stocklist_to_sql(engine)
    sync_dailydata_to_sql(engine)

'''
    stock_info = cfg.read_ini(config, 'stock')
    stock_pool = str(stock_info.get('stock_pool', None)).split()
    # print(stock_pool)
'''
if __name__ == "__main__":
    cur_path = sys.argv[0].rstrip('/sync_data.py')
    main(cur_path)
