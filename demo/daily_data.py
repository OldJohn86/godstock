#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jonathan Chen'
__date__   = '2019-09-09'

import os
import sys
import time
import datetime
from datetime import date
import tushare as ts

'''
自定义的module
'''
import cfg

'''
get daily data in stock pool
'''
def main(path):
    config = os.path.join(path, '../ts_config.ini')
#    print(config)
    stock_info = cfg.read_ini(config, 'stock')
    stock_pool = str(stock_info.get('stock_pool', None)).split()
#    print(stock_pool)
    ts_info = cfg.read_ini(config, 'tushare')
    ts_token = str(ts_info.get('cpp_token', None))
#    print(ts_token)
    pro = ts.pro_api(ts_token)
#    print(pro)
    total = len(stock_pool)
    msg = ''
    for i in range(len(stock_pool)):
        try:
            df = pro.daily(ts_code=stock_pool[i], start_date='19920101',
                    end_date=date.today().strftime('%Y%m%d'))
            df.to_excel("backup/daily_%s.xls" % str(stock_pool[i]))
            print('Seq: ' + str(i+1) + ' of ' + str(total) + ' Code: ' +
                    str(stock_pool[i]) + ' has been backup to excel!')
            msg += str(df) + '\n'
#            print(msg)
#            cfg.send_mail(config, msg)
        except Exception as err:
            print(err)

'''
获取stock daily data, backup to excel sheet
'''
if __name__ == "__main__":
    cur_path = sys.argv[0].rstrip('/daily_data.py')
#    print(cur_path)
    main(cur_path)
