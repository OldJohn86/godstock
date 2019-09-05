# -*- coding: utf-8 -*-
'''
获取stock daily data, backup to excel sheet
'''

import os
import sys
import time
import datetime
from datetime import date

import tushare as ts

# 自定的module
import cfg
import basic_data

if __name__ == "__main__":
    y_m_d = date.today().strftime('%Y%m%d')
    # print(y_m_d)

    current_path = sys.argv[0].rstrip('/daily_data.py')
    # print(current_path)
    config = os.path.join(current_path, '../ts_config.ini')
    # print(config)
    ts_info = cfg.read_ini(config, 'tushare')
    ts_token = str(ts_info.get('cpp_token', None))
    # print(ts_token)
    pro = ts.pro_api(ts_token)
    # print(pro)
    stock_info = cfg.read_ini(config, 'stock')
    stock_pool = str(stock_info.get('stock_pool', None)).split()
    # print(stock_pool)

    stocklist = basic_data.get_stocklist(ts_token)
    #total = len(stock_pool)
    total = len(stocklist)
    msg = ''
    #for i in range(len(stock_pool)):
    for i in range(len(stocklist)):
        try:
            # df = pro.daily(ts_code=stock_pool[i], start_date='19920101', end_date=date.today().strftime('%Y%m%d'))
            df = pro.daily(ts_code=stocklist[i], start_date='19920101', end_date=date.today().strftime('%Y%m%d'))
            # df = pro.daily(ts_code=stock_pool[i], start_date='20190801', end_date='20190831')
            # df.to_excel("backup/daily_%s.xls" % str(stock_pool[i]))
            df.to_excel("backup/daily_%s.xls" % str(stocklist[i]))
            # print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' + str(stock_pool[i]))
            print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' + str(stocklist[i]))

            msg += str(df) + '\n'
            # print(msg)
            # cfg.send_mail(config, msg)
        except Exception as err:
            print(err)
