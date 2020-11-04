import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import tushare as ts
import  json as js

def main():


    # left siderbar tag
    menu=['总体板块分析','北向资金分析','个股估值']

    choice=st.sidebar.selectbox('Menu',menu)


    # 根据 menu 选择显示页面内容
    if choice == '总体板块分析':
        # st.title('板块分析')
        st.header('总体板块分析')
        st.subheader('行业历史资金流')

        show_bk_buy_data()


    elif choice == '北向资金分析':

        #st.header('北向资金分析')

        choice_2=st.sidebar.selectbox("北向资金",["总体分析","板块分析"])

        # 二级菜单
        if choice_2 == '总体分析':
            st.header('北向资金分析')
            st.subheader('北向资金总体分析')
            #show_nbfbk_data()
        elif choice_2 == '板块分析':
            st.header('北向资金分析')
            st.subheader('北向资金板块持股历史数据')
            show_nbfbk_data()


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



# 显示 行业历史资金流 资料
def show_bk_buy_data():

    bk_index = json_to_str()

    #print(bk_index['板块'])
    # 将 str格式板块资料 转为 list
    bk_list = list(bk_index['板块'])   # bk_list 全部板块名

    # 显示 板块名字
    bk_choice = st.selectbox('选择板块行业：', bk_list)

    # 获取选取的板块 Code
    bk_code = bk_index['板块'][bk_choice]

    df = ts.get_bk_hist_capital_flow(bk_code)

    st.dataframe(df)


# 显示 北向资金板块持股历史 资料
def show_nbfbk_data():

    bk_index = json_to_str()

    #print(bk_index['板块'])
    # 将 str格式板块资料 转为 list
    bk_list = list(bk_index['板块'])   # bk_list 全部板块名

    # 显示 板块名字
    bk_choice = st.selectbox('选择板块行业：', bk_list)

    # 获取选取的板块 Code
    bk_code = bk_index['板块'][bk_choice]

    # 获取板块 号码
    bk_code_no=bk_code[-3:]
    #print(bk_code_no)
    df = ts.get_nbfbk_hist_capital_flow(bk_code_no)

    st.dataframe(df)


if __name__ == '__main__':
    main()
