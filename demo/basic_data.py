#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jonathan Chen'
__date__   = '2019-09-10'

'''
获取沪深A股股票代码列表并返回
'''

import os
import sys
import datetime
from datetime import date

import tushare as ts
import cfg

'''
SSE  - 上交所
SZSE - 深交所
HKEX - 港交所（未上线）
'''
exchangelist = ['SSE', 'SZSE']
# print(exchangelist)

'''
get exhcange opencal
'''
opencal = []
def get_opencal(token):
    y_m_d = date.today().strftime('%Y%m%d')
#    print(y_m_d)
    pro = ts.pro_api(token)
    for exchange in exchangelist:
        try:
            cal = pro.trade_cal(exchange=exchange, start_date='20190101', end_date='20191231')
#            print(cal)
            for row in cal.itertuples():
                if row.is_open is 1:
#                    print(row.cal_date)
                    opencal.append(str(row.cal_date))
#            print(opencal)
            cal.to_excel("backup/%s_%sopencal.xls" % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
get stocklist
'''
stocklist = []
def get_stocklist(token):
    y_m_d = date.today().strftime('%Y%m%d')
#    print(y_m_d)
    pro = ts.pro_api(token)
    for exchange in exchangelist:
        try:
            stock = pro.stock_basic(exchange=exchange, list_status='L',
                    fields='ts_code,symbol,name,area,industry,list_date')
#            print(stock)
            for row in stock.itertuples():
#                print(row.ts_code)
                stocklist.append(str(row.ts_code))
#            print(stocklist)
            stock.to_excel("backup/%s_%sstocklist.xls" % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
get companylist
'''
companylist = []
def get_companylist(token):
    y_m_d = date.today().strftime('%Y%m%d')
#    print(y_m_d)
    pro = ts.pro_api(token)
    for exchange in exchangelist:
        try:
            company = pro.stock_company(exchange=exchange,
                    fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')
#            print(stock)
            for row in company.itertuples():
#                print(row.ts_code)
                companylist.append(str(row.ts_code))
#            print(companylist)
            company.to_excel("backup/%s_%scompanylist.xls" % (exchange, y_m_d))
        except Exception as err:
            print(err)

'''
get daily data
'''
def get_dailydata(token):
    pro = ts.pro_api(token)
    total = len(stocklist)
    msg = ''
    for i in range(len(stocklist)):
        try:
            df = pro.daily(ts_code=stocklist[i], start_date='19920101',
                    end_date=date.today().strftime('%Y%m%d'))
            df.to_excel("backup/daily_%s.xls" % str(stocklist[i])[:-3])
            print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' +
                    str(stocklist[i]) + ' has been backup to excel!')
            msg += str(df) + '\n'
#            print(msg)
#            cfg.send_mail(config, msg)
        except Exception as err:
            print(err)

'''
'''
def main(path):
    config = os.path.join(path, '../ts_config.ini')
#    print(config)
    ts_info = cfg.read_ini(config, 'tushare')
    ts_token = str(ts_info.get('cpp_token', None))
#    print(ts_token)
    get_opencal(ts_token)
    get_stocklist(ts_token)
    get_companylist(ts_token)
    get_dailydata(ts_token)

if __name__ == "__main__":
    y_m_d = date.today().strftime('%Y%m%d')
#    print(y_m_d)
    cur_path = sys.argv[0].rstrip('/basic_data.py')
#    print(current_path)
    main(cur_path)
