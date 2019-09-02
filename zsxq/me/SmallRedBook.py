#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

#获取 小红书微信小程序访问抓包的 authorization
#经测试授权有效期大于6小时，最长未知
authorization = '93000000-8bbb-4999-bfff-6a33524ccccc'

def get_headers():
    headers = {
        'host': "www.xiaohongshu.com",
        'content-type': "application/json",
        'accept-language': "zh-cn",
        'accept-encoding': "br, gzip, deflate",
        'connection': "keep-alive",
        'accept': "*/*",
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN",
        'cache-control': "no-cache",
    }
    headers['authorization'] = authorization
    return headers

def querry_topics_by_keyword(keyword,page=1):
    url = "http://www.xiaohongshu.com/wx_mp_api/sns/v1/search/notes"
    querystring = {"keyword": keyword, "sort": "general", "page": page, "per_page": "20"}

    headers = get_headers()
    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def querry_detail_by_topic_id(topic_id):
    url = "http://www.xiaohongshu.com/wx_mp_api/sns/v1/note/%s/single_feed"%topic_id
    headers = get_headers()
    response = requests.request("GET", url, headers=headers)

    print(response.text)

#根据关键词和页数获取话题列表
querry_topics_by_keyword("口红",2)

#根据话题ID获取详情
querry_detail_by_topic_id('5d526f32000000002701758a')