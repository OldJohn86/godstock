# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
from datetime import date

import pymysql
from sqlalchemy import create_engine

import pandas as pd
# 自定义功能module
import cfg
import remote_mysql
import basic_data
import daily_data
import tick_data

exchangelist = ['SSE', 'SZSE']
print(exchangelist)
#SSE  - 上交所
#SZSE - 深交所
#HKEX - 港交所（未上线）

stocklist = []
if __name__ == "__main__":
    y_m_d = date.today().strftime('%Y%m%d')
    print(y_m_d)

    current_path = sys.argv[0].rstrip('/main.py')
    config = os.path.join(current_path, '../ts_config.ini')
    #print(config)
    
    stock_info = cfg.read_ini(config, 'stock')
    stock_pool = str(stock_info.get('stock_pool', None)).split()
    print(stock_pool)
    mysql_info = cfg.read_ini(config, 'mysql')
    host = str(mysql_info.get('host', None))
    user = str(mysql_info.get('user', None))
    passwd = str(mysql_info.get('passwd', None))
    database = str(mysql_info.get('database', None))

    engine = create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % (user, passwd, host, database))
    #basic cal data
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/cal_%s.xls" % str(exchange))
            # print(df)
            df.to_sql(name=str('cal_'+ exchange),con=engine,if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err)
    
    #basic stocklist data
    for exchange in exchangelist:
        try:
            df = pd.read_excel("backup/stocklist_%s.xls" % str(exchange))
            # print(df)
            for row in df.itertuples():
                #print(row.ts_code)
                stocklist.append(str(row.ts_code))
            # print(stocklist)
            df.to_sql(name=str('stocklist_'+ exchange),con=engine,if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err)

    # daily data
    # for i in range(len(stock_pool)):
    for i in range(len(stocklist)):
        try:
            # df = pd.read_excel("backup/daily_%s.xls" % str(stock_pool[i]))
            df = pd.read_excel("backup/daily_%s.xls" % str(stocklist[i]))
            # print(df)
            # df.to_sql(name=str('daily_'+ stock_pool[i]),con=engine,if_exists='replace',index=False,index_label=False)
            df.to_sql(name=str('daily_'+ stocklist[i]),con=engine,if_exists='replace',index=False,index_label=False)
        except Exception as err:
            print(err) 
