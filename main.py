import datetime
import os
import requests
import json
import base64
import re

# 配置
sub_url = [
    "https://raw.fastgit.org/freefq/free/master/v2",
    # "https://raw.fastgit.org/v2ray-links/v2ray-free/master/v2ray",
    "https://jiang.netlify.app",
    "https://shadowshare.v2cross.com/publicserver/servers/temp/SF4xoNf8GUjrHcPb",
    # "https://raw.fastgit.org/ssrsub/ssr/raw/master/V2Ray"
]


# 下载订阅链接内容将其合并
def getSubNodeContent(urls: list):
    sub_link: list[str] = []
    for i in range(len(urls)):
        url = urls[i]
        try:
            rq = requests.get(url)
            if (rq.status_code != 200):
                print("[GET Code {}] Download sub error on link: ".format(
                    rq.status_code) + url)
                continue
            print("Get node link on sub " + url)
            sub_link.append(base64.b64decode(rq.content).decode("utf-8"))
        except:
            print("[Unknown Error] Download sub error on link: " + url)

    return sub_link


# https://nodefree.org/dy/202207/20220729.txt
# 获取前两天的
for i in range(2):
    yearMonth = (datetime.datetime.now() -
                 datetime.timedelta(days=i+1)).strftime("%Y%m")
    yearMonthDay = (datetime.datetime.now() -
                    datetime.timedelta(days=i+1)).strftime("%Y%m%d")
    temp = f'https://nodefree.org/dy/{yearMonth}/{yearMonthDay}.txt'
    sub_url.append(temp)



def parseVmess(links:list):
    # 逐条读取链接，并进行测试
    country_count = {}
    merged_link = []
    for i in links:
        print(i)
        for j in i.split():
            try:
                if (j.find("vmess://") == -1):
                    continue
                # json格式化
                node = json.loads(base64.b64decode(j[8:]).decode("utf-8"))
                # 测试链接
                rq = requests.get(
                    "http://ip-api.com/json/{}?lang=zh-CN".format(node['add']))
                # 获取测试结果
                ip_info = json.loads(rq.content)
                if (ip_info['status'] != 'success'):
                    continue
                # 获取ip城市信息
                ip_country = ip_info['country']
                if (country_count.__contains__(ip_country)):
                    country_count[ip_country] += 1
                else:
                    country_count[ip_country] = 1
                newname = "{} {} {}".format(ip_country, (str)(country_count[ip_country]//10)+(
                    str)(country_count[ip_country] % 10), re.split(',| ', ip_info['org'])[0])
                # 重新写入名称
                print("Rename node {} to {}".format(node['ps'], newname))
                node['ps'] = newname
                merged_link.append(node)
            except:
                print("[Unknown Error]")
    print("Sub Merged successfully\n".format(i))
    return merged_link

def generateSubFile(merged_link: list):
    tmp = ""
    for i in merged_link:
        bs = "vmess://" + \
            base64.b64encode(json.dumps(i).encode("utf-8")).decode("utf-8")
        tmp = tmp + bs + '\n'
    res = base64.b64encode(tmp.encode("utf-8"))
    # print(res.decode("utf-8"))
    print(tmp)
    _file = open('vmess-node.txt', 'w', encoding='utf-8')
    _file.write(res.decode("utf-8"))
    _file.close()

# 下载订阅链接将其合并
sub_link = getSubNodeContent(sub_url)
vmess_link = parseVmess(sub_link)
# 合并整理完成的节点
generateSubFile(vmess_link)
