from fake_useragent import UserAgent

ua = UserAgent()
# user_agent = ua.random
# my_header = {'user-agent': user_agent}

for i in range(100):
    user_agent = ua.random
    my_header = {'user-agent': user_agent}
    print(my_header)