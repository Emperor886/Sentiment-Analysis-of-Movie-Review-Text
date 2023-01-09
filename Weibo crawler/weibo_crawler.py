import json
import requests
import csv
import time
import math

"""
Crawl Weibo user data and write data to file
"""

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    cookies = {
        "cookie": "SINAGLOBAL=7534498508000.156.1571067628282; UOR=www.takefoto.cn,widget.weibo.com,www.hfut.edu.cn; "
                  "ULV=1646732515830:83:1:1:3406649537777.8794.1646732515716:1646034864917; "
                  "XSRF-TOKEN=EmFEl_R6WzBi7OB6hadCOyLZ; SSOLoginState=1646735028; ALF=1678271030; "
                  "SCF=AhtlgZGqk4QFALwoo9q0Wmg05ROAxX-hxusgaUxhH0CxN3yOo2XVEBmkC8_Y7eR03zv1ob-9M0HVTOf4luSJgZY.; "
                  "SUB=_2A25PI17nDeRhGeFJ6VQZ9izEyDiIHXVsWTcvrDV8PUNbmtAKLUzQkW9NfFoBXTWxfFoOCOQSmKBTXk0LzTdiEHwP; "
                  "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF4Y15R6OKQ9_T-xTcu_.Fo5JpX5KzhUgL"
                  ".FoMNeoqRSozRe0B2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNS0zc1hqE1heX; "
                  "WBPSESS=jHKxeYP8s9YopP7Ymn"
                  "-kutyM3BSJ7GxkwnDpy9Xt8qxpGmhewmICjziN5St67NclbGtqboRYAXwRDC0Az1EQf_2264qTjK5dVC8mRm4KKgsHBmvvtliI_3FYgx4zaplJzEoKvAGOZJqhSwfSlvwa0A== "
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(1)
    return response.text


def save_fans_data(data):
    title = ['uid', 'id', 'screen_name', 'description', 'followers_count', 'friends_count', 'location',
             'statuses_count', 'gender']
    with open("fans_data.csv", "a", encoding="utf-8", newline="")as fi:
        fi = csv.writer(fi)
        fi.writerow([data[k] for k in title])


def save_followers_data(data):
    title = ['uid', 'id', 'screen_name', 'description', 'followers_count', 'friends_count', 'location',
             'statuses_count', 'gender']
    with open("followers_data.csv", "a", encoding="utf-8", newline="")as fi:
        fi = csv.writer(fi)
        fi.writerow([data[k] for k in title])


def get_fans_data(id):
    # 先获取总的粉丝数量
    url = "https://weibo.com/ajax/friendships/friends?relate=fans&page={}&uid={}&type=all&newFollowerCount=0"
    html = get_html(url.format(1, id))
    response = json.loads(html)
    total_number = response['total_number']
    for page in range(1, math.ceil(total_number / 20) + 1):
        html = get_html(url.format(page, id))
        response = json.loads(html)
        fans_list = response['users']
        data = {}
        for fan in fans_list:
            data['uid'] = id
            data['id'] = fan['id']  # 用户id
            data['screen_name'] = fan['screen_name']  # 用户昵称
            data['description'] = fan['description']  # 个性签名
            data['gender'] = fan['gender']  # 性别
            data['location'] = fan['location']  # 所在地
            data['followers_count'] = fan['followers_count']  # 粉丝的粉丝数量
            data['friends_count'] = fan['friends_count']  # 粉丝的关注数量
            data['statuses_count'] = fan['statuses_count']  # 粉丝的博文数量
            save_fans_data(data)


def get_followers_data(id):
    url = "https://www.weibo.com/ajax/friendships/friends?page={}&uid={}"
    html = get_html(url.format(1, id))
    response = json.loads(html)
    total_number = response['total_number']
    for page in range(1, math.ceil(total_number / 20) + 1):
        html = get_html(url.format(page, id))
        response = json.loads(html)
        fans_list = response['users']
        data = {}
        for fan in fans_list:
            data['uid'] = id
            data['id'] = fan['id']  # 用户id
            data['screen_name'] = fan['screen_name']  # 用户昵称
            data['description'] = fan['description']  # 个性签名
            data['gender'] = fan['gender']  # 性别
            data['location'] = fan['location']  # 所在地
            data['followers_count'] = fan['followers_count']  # 关注的粉丝数量
            data['friends_count'] = fan['friends_count']  # 关注的关注数量
            data['statuses_count'] = fan['statuses_count']  # 关注的博文数量
            save_followers_data(data)



if __name__ == '__main__':
    uid = ['7377392724']
    for id in uid:
        get_fans_data(id)
        get_followers_data(id)
