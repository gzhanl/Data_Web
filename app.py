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

from decimal import  *
import time

import numpy as np
import pandas as pd
import tushare as ts
import  json as js

pd.set_option('precision', 5)
np.set_printoptions(precision=8)

def main():


    # 全页显示 web app
    # st.beta_set_page_config(layout="wide")    # old setting
    st.set_page_config(layout="wide")


    # left siderbar tag
    menu=['板块资金分析','北向资金分析','个股估值']

    choice=st.sidebar.selectbox('Menu',menu)


    # 根据 menu 选择显示页面内容
    if choice == '板块资金分析':
        # st.title('板块分析')
        st.header('板块资金分析')
        #st.subheader('行业历史资金流')

        bk_code = select_bk_item()


        # 显示数据
        with st.beta_expander("板块历史资金流-Data:"):

             display_bk_buy_data(bk_code)

        # 画图
        with st.beta_expander("板块历史资金流买入比-Line Chart"):

             plot_bk_buy_LineChart(bk_code)

        # 画图
        with st.beta_expander("板块历史资金流买入占总额比-Line Chart"):

             plot_bk_buy_Ratio_LineChart(bk_code)


        with st.beta_expander("板块个股资金流(今日)"):

             display_bk_stock_cf_data(bk_code)


    elif choice == '北向资金分析':

        #st.header('北向资金分析')

        choice_2=st.sidebar.radio('北向资金',['总体分析','板块分析','个股分析'])



        # 二级菜单---------------
        if choice_2 == '总体分析':
            st.header('北向资金分析')
            st.subheader('北向资金实时数据  ')

            try:
                    df = ts.get_nf_realtime()
                    df_real_time=df[0]  # 这是实时北向资金全表
                    df_real_time=df_real_time[df_real_time["north_buy"]!='-']

                    mf=float(df_real_time.iloc[-1, 5]) / 10000  # 最后时刻的 北向净买额
                    st.subheader(df[1] +  ' ' + df_real_time.iloc[-1, 0] + ' 北向资金净买额： ' + str(mf) + '亿')  # df[1]是日期

                    st.dataframe(df_real_time.tail(5)) # 只显示最后5行
            except Exception as err_info :
                    print(err_info)
                    st.info("未有实时数据")

            # 显示数据
            with st.beta_expander("Data : 北向资金近10日净流入："):
                 df=ts.get_nf_dayline()
                 st.dataframe(df.tail(10))
                 # st.line_chart(df.tail(10)['Date'],float(df.tail(10)['north_flow']))

            with st.beta_expander("Data : 北向资金行业板块情況：" ):


                 df=ts.get_nbfbk_status()

                 # 保留14位小数位
                 getcontext().prec = 14
                 df['td_nf_ratio'] = df['td_nf_ratio'].apply(convert_to_float)


                # 保留10位小数位
                 getcontext().prec = 10

                 # df['td_increase_nf_ratio'] = df['td_increase_nf_ratio'].apply(convert_to_float)



                 st.header(df.iloc[0, 0] + '    北向资金行业板块情況  -- 以今日北资增持市值排序（td_increase_shareholding_value） ')  # df.iloc[0, 0] 时间

                 # st.info("td_stock_count:北资今日持股股票只数   td_shareholding_value：北资今日持股市值  td_bk_ratio：北资今日持股占板块比  td_nf_ratio：北资今日持股占北向资金比")

                 st.dataframe(df)

        elif choice_2 == '板块分析':
            st.header('北向资金分析')
            st.subheader('北向资金板块持股历史数据')

            bk_code = select_bk_item()






            # 显示数据
            with st.beta_expander("Data:"):

                 display_nbfbk_data(bk_code)


            # 画图
            with st.beta_expander("Line Chart"):

                plot_nbfbk_data_LineChart(bk_code)

                plot_nbf_total_bk_data_LineChart(bk_code)


        elif choice_2 == '个股分析':
                st.subheader('北向资金个股资金流')
                col1, col2 = st.beta_columns([1, 5])

                with col1:
                    stock_no = st.text_input("输入股票号码 Enter    ", max_chars=10)

                # with col2:
                #     st.subheader('  ')
                #     st.button("Go",key='1')

                st.info(stock_no)

                with st.beta_expander("沪深股通持股记录:"):


                    df = ts.get_Stock_HK_Shareholding_Today()
                    df["Shareholding_Percent"] = pd.to_numeric(df["Shareholding_Percent"])
                    df = df.sort_values('Shareholding_Percent', ascending=False)

                    col1, col2 ,col3= st.beta_columns([1,1,8])


                    Date_Shareholding = df['Date'][1]
                    Date_file=Date_Shareholding[1:5] + '-' + Date_Shareholding[6:8] + '-' + Date_Shareholding[-2:]

                    File_path='C:\\Users\\DELL\\Desktop\\Data_Web\\DownLoad_Files\\'+ Date_file

                    with col1:
                        if st.button("Download CSV"):
                            df.to_csv( File_path.strip() + '沪深股通持股记录.csv')
                            # st.success('CSV OK !')

                    with col2:
                        if st.button("Download Excel"):
                            df.to_excel( File_path.strip() + '沪深股通持股记录.xlsx')
                            # st.success('Excel OK !')

                    display_Stock_HK_Shareholding_Today()


                         # file1.write(df)
                         # file1.close()

    else:
        st.subheader('个股估值')

        col1,col2=st.beta_columns([1,5])

        with col1:
            stock_no=st.text_input("输入股票号码 Enter ",max_chars=10)

        # with col2:
        #     if st.button("Go"):
        #         dasd()




#--------------------------------------------------------------------------------------------------------------------------------------------------------------


# 读取json 档资料 转换为 str
def json_to_str():
    with open("stock_sectors_pool.json", "r", encoding='utf-8') as load_f:
         index=js.load(load_f)
    return index



# 转换小数点保留14位
def convert_to_float(value):
    if 'E-0' in value[-4:]:
        pa=value[-2:]
        pa=0.1**float(pa)
        data=float(value[:14])
        new_value=Decimal(data) * Decimal(pa)
        #new_value=value.replace('E-0','0')
    elif 'E-' in value[-3:]:
        pa=value[-2:]
        pa=0.1**float(pa)
        data=float(value[:14])
        new_value=Decimal(data) * Decimal(pa)
        #new_value=value.replace('E-0','0')
    else:new_value=value
    return new_value

# def convert_to_float2(value):




# 显示和选择板块选项
def select_bk_item():
    bk_index = json_to_str()
    # 将 str格式板块资料 转为 list
    bk_list = list(bk_index['板块'])  # bk_list 全部板块名
    # 显示 板块名字
    bk_choice = st.selectbox('选择板块行业：', bk_list)
    # 获取选取的板块 Code
    bk_code = bk_index['板块'][bk_choice]
    return bk_code



# 显示 行业历史资金流 资料
def display_bk_buy_data(bk_code):
    df=ts.get_bk_hist_capital_flow(bk_code)
    st.dataframe(df)


# 画 行业历史资金流图
def plot_bk_buy_LineChart(bk_code):
    df = ts.get_bk_hist_capital_flow(bk_code)

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
        "yAxis": [  ## 左边 Y轴
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
    st_echarts(Line_Chart,key='1')   # 设置 key值，不然一页只能一个st_echarts weights


# 画 行业历史资金流图
def plot_bk_buy_Ratio_LineChart(bk_code):
    df = ts.get_bk_hist_capital_flow(bk_code)

    # print(type(df["date"]))  #  <class 'pandas.core.series.Series'>
    #  画图 行业历史资金流
    # df["mainb_ratio_flow"]=df["mainb_ratio"]
    print(type(df['mainb_ratio']))
    # print(type(df['mainb_ratio_flow']))
    df['mainb_ratio_flow']=pd.to_numeric(df['mainb_ratio'], errors='coerce')
    df['Slargeb_ratio_flow'] = pd.to_numeric(df['Slargeb_ratio'], errors='coerce')





    # df['mainb_ratio_flow']=df['mainb_ratio_flow'].cumsum()

    df['SL_buy_ratio_flow']=df['Slargeb_ratio_flow'].cumsum()
    # df['M_SL_buy_ratio_flow']=df['M_SL_buy_ratio_flow'].cumsum()
    # print(df['mainb_ratio_flow'])
    # print(df['M_SL_buy_ratio_flow'])
    s = pd.Series([2, np.nan, 5, -1, 0])
    print(type(s))
    print(s.cumsum())


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
        "legend": {"data": ["主力买入比"]},
        "xAxis": [
            {
                "type": "category",
                "data": df["date"].tolist(),
                "axisPointer": {"type": "shadow"},
            }
        ],
        "yAxis": [  ## 左边 Y轴
            {
                "type": "value",
                "name": "比值",
                "min": -100,
                "max": 100,
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
                "data": df['SL_buy_ratio_flow'].tolist(),
            },
        ],
    }
    st_echarts(Line_Chart,key='2',height = "500px",width = "100%",)



# 显示 板块个股资金流 资料
def display_bk_stock_cf_data(bk_code):
    df=ts.get_bk_stock_capital_flow(bk_code)
    st.dataframe(data=df,width=2000, height=2000)



# 显示 北向资金板块历史资金流 资料
def display_nbfbk_data(bk_code):
    # 获取板块 号码
    bk_code_no = bk_code[-3:]
    # print(bk_code_no)
    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)
    # df=get_nbfbk_data(bk_code)
    st.dataframe(df)


#  画图 当前板块北向资金占总北向资金比
def plot_nbfbk_data_LineChart(bk_code):
    bk_code_no = bk_code[-3:]
    # print(bk_code_no)
    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    df = df.drop(index=[0])  # 去除 None 值 ，不然 max() 失效
    print(df)
    col1, col2, col3 = st.beta_columns([1, 1, 1])

    min_value = df["znzjb"].astype(str).min()
    # min_value = float(min_value) * 0.97
    min_value = round(float(min_value) * 0.97 ,4 )


    print(min_value)

    max_value = df["znzjb"].astype(str).max(skipna=True)
    max_value = round(float(max_value) * 1.03 , 4)

    print(max_value)

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
                "magicType": {"show": True, "type": ["line", "bar"]},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
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


#  画图 当前板块北向资金占板块（A股）比
def plot_nbf_total_bk_data_LineChart(bk_code):
    bk_code_no = bk_code[-3:]
    # print(bk_code_no)
    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    df = df.drop(index=[0])  # 去除 None 值 ，不然 max() 失效
    print(df)
    col1, col2, col3 = st.beta_columns([1, 1, 1])

    min_value = df["cgbkb"].astype(str).min()
    # min_value = float(min_value) * 0.97
    min_value = round(float(min_value) * 0.97 ,4 )


    print(min_value)

    max_value = df["cgbkb"].astype(str).max(skipna=True)
    max_value = round(float(max_value) * 1.03 , 4)

    print(max_value)

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
                "magicType": {"show": True, "type": ["line", "bar"]},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
            }
        },
        "legend": {"data": ["北向资金持股占总板块资金比", "", ""]},
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
                "interval": 0.002,
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
                "name": "北向资金持股占总板块资金比",
                "type": "line",
                "color":"orange",
                "yAxisIndex": 0,
                "data": df["cgbkb"].sort_index(ascending=False).tolist(),
            },
        ],
    }
    st_echarts(Line_Chart)


# 显示 滬股通及深股通持股紀錄 今日
def display_Stock_HK_Shareholding_Today():

    df = ts.get_Stock_HK_Shareholding_Today()
    Date_Shareholding=df['Date'][1]

    # #####
    # 重点：排序之前 ,先要将列类型改成 to_numberic
    # #####

    df["Shareholding_Percent"] = pd.to_numeric(df["Shareholding_Percent"])
    df = df.sort_values('Shareholding_Percent',ascending=False)
    # st.dataframe(df)
    st.subheader('持股日期：' + Date_Shareholding )
    st.dataframe(data=df, height=1000)




if __name__ == '__main__':
    main()
