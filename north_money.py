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


#  画图 当前個股佔交易所（A股）百分比
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