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
import numpy as np
import pandas as pd
import tushare as ts
import  json as js

def main():


    # 全页显示 web app
    # st.beta_set_page_config(layout="wide")    # old setting
    st.set_page_config(layout="wide")


    # left siderbar tag
    menu=['总体板块分析','北向资金分析','个股估值']

    choice=st.sidebar.selectbox('Menu',menu)


    # 根据 menu 选择显示页面内容
    if choice == '总体板块分析':
        # st.title('板块分析')
        st.header('总体板块分析')
        st.subheader('行业历史资金流')

        bk_code = select_bk_item()


        # 显示数据
        with st.beta_expander("Data:"):
             show_bk_buy_data(bk_code)

        # 画图
        with st.beta_expander("Line Chart"):
            df=get_bk_buy_data(bk_code)

            # print(type(df["date"]))  #  <class 'pandas.core.series.Series'>
            #  画图 行业历史资金流
            Line_Chart = {
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
                },
                "toolbox": {
                    "feature": {
                        "dataView": {"show": True, "readOnly": False},
                        "magicType": {"show": True, "type": ["line", "bar"]},
                        "restore": {"show": True},
                        "saveAsImage": {"show": True},
                    }
                },
                "legend": {"data": ["主力买入比", "降水量", "平均温度"]},
                "xAxis": [
                    {
                        "type": "category",
                        "data": df["date"].tolist(),
                        "axisPointer": {"type": "shadow"},
                    }
                ],
                "yAxis": [   ## 左边 Y轴
                    {
                        "type": "value",
                        "name": "比值",
                        "min": -20,
                        "max": 20,
                        "interval": 5,
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
                        "name": "主力买入比",
                        "type": "line",
                        "yAxisIndex": 0,
                        "data": df["mainb_ratio"].tolist(),
                    },
                ],
            }
            st_echarts(Line_Chart)

    elif choice == '北向资金分析':

        #st.header('北向资金分析')

        choice_2=st.sidebar.radio("北向资金",["总体分析","板块分析"])



        # 二级菜单---------------
        if choice_2 == '总体分析':
            st.header('北向资金分析')
            st.subheader('北向资金实时数据  ')

            df = ts.get_nf_realtime()
            df_real_time=df[0]  # 这是实时北向资金全表
            df_real_time=df_real_time[df_real_time["north_buy"]!='-']

            mf=float(df_real_time.iloc[-1, 5]) / 10000  # 最后时刻的 北向净买额
            st.subheader(df[1] +  ' ' + df_real_time.iloc[-1, 0] + ' 北向资金净买额： ' + str(mf) + '亿')  # df[1]是日期


            st.dataframe(df_real_time.tail(5)) # 只显示最后5行


            # 显示数据
            with st.beta_expander("Data : 北向资金近10日净流入："):
                 df=ts.get_nf_dayline()
                 st.dataframe(df.tail(10))
                 # st.line_chart(df.tail(10)['Date'],float(df.tail(10)['north_flow']))

            with st.beta_expander("Data : 北向资金行业板块情況：" ):
                 df=ts.get_nbfbk_status()
                 st.header(df.iloc[0, 0] + '    北向资金行业板块情況')
                 st.dataframe(df)

        elif choice_2 == '板块分析':
            st.header('北向资金分析')
            st.subheader('北向资金板块持股历史数据')

            bk_code = select_bk_item()

            # 显示数据
            with st.beta_expander("Data:"):
                 show_nbfbk_data(bk_code)


            # 画图
            with st.beta_expander("Line Chart"):
                 df = get_nbfbk_data(bk_code)

                 df=df.drop(index=[0])   # 去除 None 值 ，不然 max() 失效
                 print(df)
                 col1, col2, col3 = st.beta_columns([1, 1 ,1])


                 min_value=df["znzjb"].astype(str).min()
                 min_value=float(min_value) * 0.97

                 print(min_value)



                 max_value=df["znzjb"].astype(str).max( skipna = True)
                 max_value=float(max_value)* 1.03

                 print(max_value)

                 with col1:
                     min_scale = st.slider('MIN', 0.000, 1.000, min_value, 0.005)


                 with col2:
                     max_scale = st.slider('MAX', 0.000, 1.000, max_value, 0.005)



                 Line_Chart = {
                        "tooltip": {
                            "trigger": "axis",
                            "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
                        },
                        "toolbox": {
                            "feature": {
                                "dataView": {"show": True, "readOnly": False},
                                "magicType": {"show": True, "type": ["line", "bar"]},
                                "restore": {"show": True},
                                "saveAsImage": {"show": True},
                            }
                        },
                        "legend": {"data": ["持股占北向资金比", "", ""]},
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
                                "min": min_scale,
                                "max": max_scale,
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
                                "name": "持股占北向资金比",
                                "type": "line",
                                "yAxisIndex": 0,
                                "data": df["znzjb"].sort_index(ascending=False).tolist(),
                            },
                        ],
                    }
                 st_echarts(Line_Chart)


    else:
        st.subheader('个股估值')

        col1,col2=st.beta_columns([3,1])

        with col1:
            stock_no=st.text_input("输入股票号码",max_chars=10)

        with col2:
            if st.button("Go"):
                dasd()

# 读取json 档资料 转换为 str
def json_to_str():
    with open("stock_sectors_pool.json", "r", encoding='utf-8') as load_f:
         index=js.load(load_f)
    return index


# 选择板块选项
def select_bk_item():
    bk_index = json_to_str()
    # 将 str格式板块资料 转为 list
    bk_list = list(bk_index['板块'])  # bk_list 全部板块名
    # 显示 板块名字
    bk_choice = st.selectbox('选择板块行业：', bk_list)
    # 获取选取的板块 Code
    bk_code = bk_index['板块'][bk_choice]
    return bk_code

# 获取 行业历史资金流 资料
def get_bk_buy_data(bk_code):
    df = ts.get_bk_hist_capital_flow(bk_code)
    return df


# 显示 行业历史资金流 资料
def show_bk_buy_data(bk_code):
    df=get_bk_buy_data(bk_code)
    st.dataframe(df)


# # 获取 北向资金總體板块持股情況
# def get_nbfbk_status( ):
#     # 获取板块 号码
#     df = ts.get_nbfbk_hist_capital_flow(bk_code_no)
#
#     return df



# 获取 北向资金板块持股历史 资料
def get_nbfbk_data(bk_code):
    # 获取板块 号码
    bk_code_no=bk_code[-3:]
    #print(bk_code_no)
    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    return df



# 显示 北向资金板块持股历史 资料
def show_nbfbk_data(bk_code):
    df=get_nbfbk_data(bk_code)

    st.dataframe(df)


#  画图 行业历史资金流


if __name__ == '__main__':
    main()
