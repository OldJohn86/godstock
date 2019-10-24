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
import tick_data
import remote_mysql
import basic_data
import daily_data
import sync_data

'''
SSE  - 上交所
SZSE - 深交所
HKEX - 港交所（未上线)
'''
exchangelist = ['SSE', 'SZSE']
print(exchangelist)

def backup_all_to_excel(path):
    basic_data.main(path)

def sync_all_to_sql(path):
    sync_data.main(path)

if __name__ == "__main__":
    cur_path = sys.argv[0].rstrip('/main.py')
    backup_all_to_excel(cur_path)
    sync_all_to_sql(cur_path)

