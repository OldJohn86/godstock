'''
获取沪深A股股票代码列表并返回
'''
import os
import sys
import datetime
from datetime import date

import tushare as ts
import cfg

exchangelist = ['SSE', 'SZSE']
print(exchangelist)
#SSE  - 上交所
#SZSE - 深交所
#HKEX - 港交所（未上线）

def get_cal(token):
    pro = ts.pro_api(token)
    for exchange in exchangelist:
        try:
            cal = pro.trade_cal(exchange=exchange, start_date='20190101', end_date='20191231')
            print(cal)
            cal.to_excel("backup/cal_%s.xls" % exchange)
        except Exception as err:
            print(err)

def get_stocklist(token):
    pro = ts.pro_api(token)
    for exchange in exchangelist:
        try:
            stock = pro.stock_basic(exchange=exchange, list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            #print(stock)
            for row in stock.itertuples():
                #print(row.ts_code)
                stocklist.append(str(row.ts_code))
            # print(stocklist)
            stock.to_excel("backup/stocklist_%s.xls" % exchange)
        except Exception as err:
            print(err)
    return stocklist

stocklist = []
if __name__ == "__main__":
    y_m_d = date.today().strftime('%Y%m%d')
    # print(y_m_d)

    current_path = sys.argv[0].rstrip('/basic_data.py')
    # print(current_path)
    config = os.path.join(current_path, '../ts_config.ini')
    print(config)
    ts_info = cfg.read_ini(config, 'tushare')
    ts_token = str(ts_info.get('cpp_token', None))
    # print(ts_token)
    
    # get_cal(ts_token)
    stocklist = get_stocklist(ts_token)
    print(stocklist)
