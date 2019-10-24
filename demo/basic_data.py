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
print(exchangelist)

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
    return opencal

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
    return stocklist

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
    return companylist

def main(path):
    config = os.path.join(path, '../ts_config.ini')
#    print(config)
    ts_info = cfg.read_ini(config, 'tushare')
    ts_token = str(ts_info.get('cpp_token', None))
#    print(ts_token)
    opencal = get_opencal(ts_token)
    stocklist = get_stocklist(ts_token)
    companylist = get_companylist(ts_token)
    return (opencal, stocklist, companylist)

if __name__ == "__main__":
    y_m_d = date.today().strftime('%Y%m%d')
#    print(y_m_d)
    cur_path = sys.argv[0].rstrip('/basic_data.py')
#    print(current_path)
    (opencal, stocklist, companylist) = main(cur_path)
    print(opencal)
    print(stocklist)
    print(companylist)
