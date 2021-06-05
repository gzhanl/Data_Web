import tushare as ts

token = '67bcc08d60c4287441a1a80dd58701c5fd2d2c916bbf6758bb9cc05d'

pro = ts.pro_api(token)

#获取单日全部持股
df1 = pro.hk_hold(trade_date='20210604')

print(df1)

df1.to_csv('TS_Code_Table.csv')
# #获取单日交易所所有持股
# df2 = pro.hk_hold(trade_date='20190625', exchange='SH')
# print(df2)