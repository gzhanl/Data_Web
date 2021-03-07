# from decimal import  *
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
import  os
print(os.getcwd())  # C:\Users\DELL\Desktop\ST_Web_App\App
# print(os.path.dirname(__file__))


print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
app_path=os.path.abspath(os.path.dirname(os.getcwd()))
print(app_path)