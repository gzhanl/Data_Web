# from decimal import  *
import  os
import  json as js
import tushare as ts
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import Bar , Line
from streamlit_echarts import st_pyecharts
import plotly.figure_factory as ff

from multiprocessing import Pool
import os
from decimal import  *
import time

import numpy as np
import pandas as pd
import tushare as ts
import  json as js
# getcontext().prec=8
# a='9.78934558435788E-05'
#
# # 转换小数点保留6位
# def convert_to_float(value):
#     if 'E-0' in value[-4:]:
#         pa=value[-2:]
#         pa=0.1**float(pa)
#         data=float(value[:6])
#         new_value=Decimal(data) * Decimal(pa)
#         #new_value=value.replace('E-0','0')
#     return new_value
#
#
# print(convert_to_float(a))

# print(os.getcwd())  # C:\Users\DELL\Desktop\ST_Web_App\App
# # print(os.path.dirname(__file__))
#
#
# print(os.path.abspath(os.path.dirname(__file__)))
# print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
# app_path=os.path.abspath(os.path.dirname(os.getcwd()))
# print(app_path)
# import tushare as ts
# bk_code_no=420
# res=ts.update_nbfbk_hist_capital_flow_CSV(bk_code_no)


# def json_to_str():
#
#     App_path = os.path.abspath(os.path.dirname(os.getcwd()))
#
#     with open(App_path + '\\Data\\json\\stock_sectors_pool.json', 'r', encoding='utf-8') as load_f:
#          index=js.load(load_f)
#     return index
#
#
# bk_index = json_to_str()
# # 将 str格式板块资料 转为 list
# bk_list = list(bk_index['板块'])  # bk_list 全部板块名
#
# dfs = {}
# df_list = []
# # bk_code = bk_index['板块'][bk_choice]
#
# App_path = os.path.abspath(os.path.dirname(os.getcwd()))
#
# File_path = App_path + '\\Data\\Industry_data\\'
#
# # df.to_csv(File_path.strip() + '沪深股通持股记录.csv')
#
# for bk_name in bk_list:
#   try :
#       bk_code = bk_index['板块'][bk_name]
#       bk_code_no = bk_code[-3:]
#       # df=ts.get_nbfbk_hist_capital_flow(bk_code_no)
#       dfs['df_{}'.format(bk_code_no)] = ts.get_nbfbk_hist_capital_flow(bk_code_no)
#       dfs['df_{}'.format(bk_code_no)]=dfs['df_{}'.format(bk_code_no)].sort_index(ascending=False)
#       # ts.update_nbfbk_hist_capital_flow_CSV(bk_code_no)
#       # df_list.append(dfs['df_{}'.format(bk_code_no)])
#       # dfs['df_{}'.format(bk_code_no)].dropna(axis=0, how='any', inplace=True)
#       dfs['df_{}'.format(bk_code_no)].to_csv( File_path + bk_code_no +'_nfbk.csv',index=False)
#       # print(df_list)
#   except Exception as e:
#       pass
#   continue
# # df = pd.concat(df_list)
# # df.dropna(axis=0, how='any', inplace=True)
# #
# # File_path = 'C:\\Users\\DELL\\Desktop\\Data_Web\\Data\\'
# # # df.to_excel(File_path.strip() + 'nfbk_trend.xlsx')
# # pd.read_excel(File_path.strip() + 'nfbk_trend.xlsx')
#
# print("Finish ! ")
#
def json_to_str():

    App_path = os.path.abspath(os.path.dirname(os.getcwd()))

    with open(App_path + '\\Data\\json\\stock_sectors_pool.json', 'r', encoding='utf-8') as load_f:
         index=js.load(load_f)
    return index

def map_fun(bk_code_no):
    # 将 str格式板块资料 转为 list

    try:

        # df=ts.get_nbfbk_hist_capital_flow(bk_code_no)
        # dfs['df_{}'.format(bk_code_no)] = ts.update_nbfbk_hist_capital_flow_CSV(bk_code_no)
        ts.update_nbfbk_hist_capital_flow_CSV(bk_code_no)
        # df_list.append(dfs['df_{}'.format(bk_code_no)])
        # dfs['df_{}'.format(bk_code_no)].dropna(axis=0, how='any', inplace=True)
        # dfs['df_{}'.format(bk_code_no)].to_csv( File_path + bk_code_no +'_nfbk.csv',index=False)
        # print(df_list)
    except Exception as e:
        pass


def update_data_multi():
    bk_index = json_to_str()
    bk_list = list(bk_index['板块'])  # bk_list 全部板块名


    App_path = os.path.abspath(os.path.dirname(os.getcwd()))

    File_path = App_path + '\\Data\\Industry_data\\'

    pool = Pool(2)
    # itr_arg =[ bk_name for bk_name in bk_list]
    for bk_name in bk_list:
        bk_code = bk_index['板块'][bk_name]
        bk_code_no = bk_code[-3:]
        pool.apply_async(map_fun,args=(bk_code_no,))

    # pool.map(map_fun,bk_code_no)
    pool.close()
    pool.join()





update_data_multi()


# # ---------------------------------------------------------
#
# from multiprocessing import Pool
# import os, time, random
#
#
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#
#
# if __name__ == '__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(4)  # 创建4个进程
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i,))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()

