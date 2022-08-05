import re

# from main import parseVmess


list_a = ["1", "2"]

str_1="ssr://123"

reg = r'.*://'

res = re.match(reg, str_1)
if res:
    print(res.group(0))
else:
    print(res)

print(str_1.find("://"))

print(str_1[3+3:])

print("http://ip-api.com/json/{}?lang=zh-CN".format("adada"))

# parseVmess(["vmess://eyJhZGQiOiJsbXMudWluLWFudGFzYXJpLmFjLmlkIiwiYWlkIjoiMCIsImhvc3QiOiJiaXpuZXQtcy5uZXh0dnBuLmNjIiwiaWQiOiI0NmJmZGI1OS04M2M2LTQ"])