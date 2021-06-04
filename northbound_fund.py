"""
北向资金的相关功能


"""

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import matplotlib.pyplot as plt
import streamlit as st
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



# 显示 北向资金板 -- 块历史资金流数据
def display_nbfbk_data(bk_code):
    # 获取板块 号码
    bk_code_no = bk_code[-3:]
    # print(bk_code_no)

    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    # df = ts.get_nbfbk_hist_capital_flow_CSV(bk_code_no)

    # df=get_nbfbk_data(bk_code)
    st.dataframe(df)




#  画折线图 -- 当前板块北向资金  占  总北向资金 比值
def plot_nbfbk_data_LineChart(bk_code):
    bk_code_no = bk_code[-3:]
    # print(bk_code_no)
    # df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    # df = ts.get_nbfbk_hist_capital_flow_CSV(bk_code_no)


    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)
    df = df.drop(index=[0])  # 去除 None 值 ，不然 max() 失效
    # print(df)
    # col1, col2, col3 = st.beta_columns([1, 1, 1])

    min_value = df["znzjb"].astype(str).min()
    # min_value = float(min_value) * 0.97
    min_value = round(float(min_value) * 0.97 ,4 )


    # print(min_value)

    max_value = df["znzjb"].astype(str).max(skipna=True)
    max_value = round(float(max_value) * 1.03 , 4)

    # print(max_value)

    # with col1:
    #     min_scale = st.slider('MIN', 0.000, 1.000, min_value, 0.005)
    #
    # with col2:
    #     max_scale = st.slider('MAX', 0.000, 1.000, max_value, 0.005)

    Line_Chart = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
        },
        "toolbox": {
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ['line', 'bar', 'stack', 'tiled']},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
                "dataZoom": {"show": True}
            }
        },
        "legend": {"data": ["北向资金持股占总北向资金比", "", ""]},
        "xAxis": [
            {
                "type": "category",
                "data": df["date"].sort_index(ascending=False).tolist(),
                "axisPointer": {"type": "shadow"},
            }
        ],
        "yAxis": [  ## 左边 Y轴
            {
                "type": "value",
                "name": "比值",
                "min": min_value,
                "max": max_value,
                "interval": 0.01,
                "axisLabel": {"formatter": "{value} "},
            },
            # {       ## 右边 Y轴
            #     "type": "value",
            #     "name": "温度",
            #     "min": 0,
            #     "max": 25,
            #     "interval": 5,
            #     "axisLabel": {"formatter": "{value} °C"},
            # },
        ],
        "series": [
            {
                "name": "北向资金持股占总北向资金比",
                "type": "line",
                "yAxisIndex": 0,
                "data": df["znzjb"].sort_index(ascending=False).tolist(),
            },
        ],
    }
    st_echarts(Line_Chart)



#  画折线图 -- 当前個股佔交易所（A股）百分比
def plot_stock_in_nbf_Shareholding_Percent_LineChart(df_stock):

    Stock_Name = df_stock.iloc[1,3]  # 獲取第第3列 第1個數
    # df.iloc[0, 0]
    # print(Stock_Name)
    # min_value = df_stock["Shareholding_Percent"].astype(str).min()
    min_value = df_stock["Shareholding_Percent"].min()

    # min_value = float(min_value) * 0.97
    min_value = round(float(min_value) * 0.97 ,2 )

    # print(min_value)

    # max_value = df_stock["Shareholding_Percent"].astype(str).max(skipna=True)
    max_value = df_stock["Shareholding_Percent"].max()
    max_value = round(float(max_value) * 1.03 , 2)

    # print(max_value)

    # with col1:
    #     min_scale = st.slider('MIN', 0.000, 1.000, min_value, 0.005)
    #
    # with col2:
    #     max_scale = st.slider('MAX', 0.000, 1.000, max_value, 0.005)

    Line_Chart = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
        },
        "toolbox": {
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ['line', 'bar', 'stack', 'tiled']},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
                "dataZoom": {"show": True}
            }
        },
        "legend": {"data": [ Stock_Name + "--滬深港通持股占A股比", "", ""]},
        "xAxis": [
            {
                "type": "category",
                "data": df_stock["Date"].sort_index(ascending=True).tolist(),
                "axisPointer": {"type": "shadow"},
            }
        ],
        "yAxis": [  ## 左边 Y轴
            {
                "type": "value",
                "name": "比值",
                "min": min_value,
                "max": max_value,
                "interval": 1,
                "axisLabel": {"formatter": "{value} "},
            },
            # {       ## 右边 Y轴
            #     "type": "value",
            #     "name": "温度",
            #     "min": 0,
            #     "max": 25,
            #     "interval": 5,
            #     "axisLabel": {"formatter": "{value} °C"},
            # },
        ],
        "series": [
            {
                "name": Stock_Name + "--滬深港通持股占A股比",
                "type": "line",
                "color":"blue",
                "yAxisIndex": 0,
                "data": df_stock["Shareholding_Percent"].sort_index(ascending=True).tolist(),
            },
        ],
    }
    st_echarts(Line_Chart)