import requests
import time
import re
import pandas as pd
from datetime import datetime



my_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}  # my browser

def A_stock_in_HK_ratio_by_dates():

    url_sh = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'  # 滬股通

    url_sz = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'  # 深股通

    today_date = datetime.today().strftime('%Y%m%d')
    # date='2021/01/18'
    dates=['2021/01/09','2021/01/18']
    res_all=''

    for url in [url_sh,url_sz]:

        for date in dates:

            post_data = {
                '__VIEWSTATE': '/wEPDwUJNjIxMTYzMDAwZGQ79IjpLOM+JXdffc28A8BMMA9+yg==',
                '__VIEWSTATEGENERATOR': 'EC4ACD6F',
                '__EVENTVALIDATION': '/wEdAAdtFULLXu4cXg1Ju23kPkBZVobCVrNyCM2j+bEk3ygqmn1KZjrCXCJtWs9HrcHg6Q64ro36uTSn/Z2SUlkm9HsG7WOv0RDD9teZWjlyl84iRMtpPncyBi1FXkZsaSW6dwqO1N1XNFmfsMXJasjxX85jz8PxJxwgNJLTNVe2Bh/bcg5jDf8=',
                'today': today_date,
                'sortBy': 'stockcode',
                'sortDirection': 'asc',
                'alertMsg': '',
                'txtShareholdingDate': date,
                'btnSearch': '搜尋'
            }

            res = requests.post(url, data=post_data , headers=my_header, timeout=10).text

            res_all=res_all + res
            res=''
    print(res_all)
    return res_all


def A_stock_in_HK_ratio_by_today():

    url_sh = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'  # 滬股通

    url_sz = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'  # 深股通

    today_date = datetime.today().strftime('%Y%m%d')

    res_all=''

    for url in [url_sh,url_sz]:

            post_data = {
                '__VIEWSTATE': '/wEPDwUJNjIxMTYzMDAwZGQ79IjpLOM+JXdffc28A8BMMA9+yg==',
                '__VIEWSTATEGENERATOR': 'EC4ACD6F',
                '__EVENTVALIDATION': '/wEdAAdtFULLXu4cXg1Ju23kPkBZVobCVrNyCM2j+bEk3ygqmn1KZjrCXCJtWs9HrcHg6Q64ro36uTSn/Z2SUlkm9HsG7WOv0RDD9teZWjlyl84iRMtpPncyBi1FXkZsaSW6dwqO1N1XNFmfsMXJasjxX85jz8PxJxwgNJLTNVe2Bh/bcg5jDf8=',
                'today': today_date,
                'sortBy': 'stockcode',
                'sortDirection': 'asc',
                'alertMsg': '',
                'txtShareholdingDate': '',
                'btnSearch': '搜尋'
            }

            res = requests.get(url, data=post_data , headers=my_header, timeout=10).text

            res_all=res_all + res

    # p_stock_code='<td class="col-stock-code">(.*?)</td>'
    # p_stock_name = '<td class="col-stock-name">(.*?)</td>'
    # p_shareholding = '<td class="col-shareholding">(.*?)</td>'
    # p_shareholding_percent = '<td class="col-shareholding-percent">(.*?)</td>'


    data= re.findall('<div class="mobile-list-body">(.*?)</div>',res_all,re.S)
    # for i in range(len(data)):
    #     data = data[i].replace('%', "")
    # stock_name = re.findall(p_stock_name,res_all,re.S)
    # stock_name = re.findall('<div class="mobile-list-body">(.*?)</div>', res_all, re.S)
    #
    # shareholding = re.findall(p_shareholding, res_all, re.S)
    # shareholding = re.findall('<div class="mobile-list-body">(.*?)</div>', res_all, re.S)
    #
    # shareholding_percent = re.findall(p_shareholding_percent, res_all, re.S)
    # shareholding_percent = re.findall('<div class="mobile-list-body">(.*?)</div>', res_all, re.S)

    #将 list 按每组4个分开
    step = 4
    flows = [data[i:i + step] for i in range(0, len(data), step)]

    # flows = []
    # for i in range(len(stock_code)):
    #     # stock_code[i] = re.findall('<div class="mobile-list-body">(.*?)</div>', stock_code[i])
    #     # stock_name[i] = re.findall('<div class="mobile-list-body">(.*?)</div>', stock_name[i])
    #     # shareholding[i] = re.findall('<div class="mobile-list-body">(.*?)</div>', shareholding[i])
    #     # shareholding_percent[i] = re.findall('<div class="mobile-list-body">(.*?)</div>', shareholding_percent[i])
    #
    for flow in flows :
        flow[3]=flow[3].replace('%', "")

    # flows.append(flow)

    df = pd.DataFrame(flows)
    columns = {0: "Stock_Code", 1: "Stock_Name", 2: "Shareholding", 3: "Shareholding_Percent"}

    df.rename(columns=columns, inplace=True)
    # df=df.sort_values(by=['Shareholding_Percent'],ascending=False)
    print(df)
    # print(stock_code)
    # print(res_all)
    return res_all




file1=open('C:\\Users\\DELL\\Desktop\\Data_Web\\res_today.csv','w')
file1.write(A_stock_in_HK_ratio_by_today())
file1.close()