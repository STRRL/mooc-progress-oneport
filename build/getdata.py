# -*- coding:utf-8 -*-
import ConfigParser, os, sys, requests, time, commands
from contextlib import closing

datadic = {}
reqs = []
dirpath = sys.path[0] + "/../app"


def getConfig(key):
    config = ConfigParser.ConfigParser()
    confpath = sys.path[0] + "/user.conf"
    config.read(confpath)
    config.sections()
    return config.get('accont', key)


def DownloadFile(username, password, classid, alias):
    global dirpath
    s = requests.Session()
    url = "https://studio-ynu.xuetangx.com/signin"
    headers = {
        'authorization': "Basic eHVldGFuZ1hjbG91ZDp4dWV0YW5nWGNsb3Vk",
        'cache-control': "no-cache"
    }
    response = s.request("GET", url, headers=headers)
    datadic['csrftoken'] = response.cookies.get(name='csrftoken')

    url = "http://studio-ynu.xuetangx.com/login_post"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"honor_code\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (
        username, password)
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'authorization': "Basic eHVldGFuZ1hjbG91ZDp4dWV0YW5nWGNsb3Vk",
        'x-requested-with': "XMLHttpRequest",
        'x-csrftoken': "%s" % datadic['csrftoken'],
        'cache-control': "no-cache"
    }
    response = s.request("POST", url, data=payload, headers=headers, cookies=datadic)
    # print response.content

    # url = "http://studio-ynu.xuetangx.com/statistics/2.1/download/data/study_progress/%s" % classid
    url = "http://studio-ynu.xuetangx.com/statistics/2.1/interface/data_download?file_format=xlsx&group_key=2&data_type=video&course_id=%s" % classid
    headers = {
        'authorization': "Basic eHVldGFuZ1hjbG91ZDp4dWV0YW5nWGNsb3Vk",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cache-control': "no-cache"
    }
    with closing(s.get(url, headers=headers, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        commands.getstatusoutput('rm %s/src/%s -rf' % (dirpath, alias))
        os.mkdir(dirpath + "/src/%s" % alias)
        with open(dirpath + "/src/%s/file.xlsx" % alias, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                if data:
                    file.write(data)


def unzipFile(alias):
    # (s, o) = commands.getstatusoutput('rm %s/src/%s/study* -rf' % (dirpath, alias))
    # print o
    (s, o) = commands.getstatusoutput(
        'tar -zxvf %s/src/%s/file.tar.gz -C%s/src/%s/' % (dirpath, alias, dirpath, alias))
    return


# def start():
#     DownloadFile()
#     unzipFile()

def start(username, password, classid, alias):
    DownloadFile(username, password, classid, alias)
    # unzipFile(alias)
