import random

import requests
from datetime import datetime
import json
import time
import pandas as pd
import os
from bs4 import BeautifulSoup
class WxMps(object):
    """微信公众号文章、评论抓取爬虫"""

    def __init__(self, _biz, _pass_ticket, _app_msg_token, _cookie, _offset=0,_savepath='.',_cols=[]):
        self.offset = _offset
        self.biz = _biz  # 公众号标志
        self.msg_token = _app_msg_token  # 票据(非固定)
        self.pass_ticket = _pass_ticket  # 票据(非固定)
        self.savepath=_savepath
        self.columns=_cols

        self.headers = {
            'Cookie': _cookie,  # Cookie(非固定)
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1219.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1219.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1219.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'

        }
        wx_mps = 'wxmps'  # 这里数据库、用户、密码一致(需替换成实际的)
        # self.postgres = pgs.Pgs(host='localhost', port='5432', db_name=wx_mps, user=wx_mps, password=wx_mps)
    def log(self):
        time.strftime('%Y-%m%d %H:%M:%S')
    def start(self):
        """请求获取公众号的文章接口"""

        offset = self.offset
        while True:
            api = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={0}&f=json&offset={1}' \
                  '&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket={2}&wxtoken=&appmsg_token' \
                  '={3}&x5=1&f=json'.format(self.biz, offset, self.pass_ticket, self.msg_token)

            # api = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={0}&f=json&offset={1}' \
            #       '&count=10&is_ok=1&scene=7&uin=MjIzMzM0ODAzNw==&key=777&pass_ticket={2}&wxtoken=&appmsg_token' \
            #       '={3}&x5=1&f=json'.format(self.biz, offset, self.pass_ticket, self.msg_token)

            resp = requests.get(api, headers=self.headers).json()
            ret, status = resp.get('ret'), resp.get('errmsg')  # 状态信息
            if ret == 0 or status == 'ok':
                print('Crawl article: ' + api)
                offset = resp['next_offset']  # 下一次请求偏移量
                general_msg_list = resp['general_msg_list']
                msg_list = json.loads(general_msg_list)['list']  # 获取文章列表
                for msg in msg_list:
                    comm_msg_info = msg['comm_msg_info']  # 该数据是本次推送多篇文章公共的
                    msg_id = comm_msg_info['id']  # 文章id
                    post_time = datetime.fromtimestamp(comm_msg_info['datetime'])  # 发布时间
                    # msg_type = comm_msg_info['type']  # 文章类型
                    # msg_data = json.dumps(comm_msg_info, ensure_ascii=False)  # msg原数据

                    app_msg_ext_info = msg.get('app_msg_ext_info')  # article原数据
                    if app_msg_ext_info:
                        # 本次推送的首条文章
                        self._parse_articles(app_msg_ext_info, msg_id, post_time)
                        # 本次推送的其余文章
                        multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                        if multi_app_msg_item_list:
                            for item in multi_app_msg_item_list:
                                msg_id = item['fileid']  # 文章id
                                if msg_id == 0:
                                    msg_id = int(time.time() * 1000)  # 设置唯一id,解决部分文章id=0出现唯一索引冲突的情况
                                self._parse_articles(item, msg_id, post_time)
                print('next offset is %d' % offset)
            else:
                print('Before break , Current offset is %d' % offset)
                break

    def _parse_articles(self, info, msg_id, post_time):
        """解析嵌套文章数据并保存入库"""

        title = info.get('title')  # 标题
        cover = info.get('cover')  # 封面图
        author = info.get('author')  # 作者
        digest = info.get('digest')  # 关键字
        source_url = info.get('source_url')  # 原文地址
        content_url = info.get('content_url')  # 微信地址
        content_html = self.get_content(content_url)  # 微信内容
        row=[title,cover,author,digest,source_url,content_url,content_html]
        df=pd.DataFrame(data=[row],columns=self.columns)
        # df.to_csv(self.savepath,mode='a',encoding='utf-8',header=not os.path.exists('%s/article.list.csv'))
        df.to_csv('{0}/article.list.csv'.format(self.savepath), mode='a', encoding='utf-8',
                  header=not os.path.exists('{0}/article.list.csv'.format(self.savepath)))



    def get_content(self,url):
        rtime=random.randint(120,180)
        time.sleep(rtime)
        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser', from_encoding='utf-8')
        #文章内容 html
        content_html=soup.find(id='js_content')
        return content_html
    @staticmethod
    def _save_article():
        sql = 'insert into tb_article(msg_id,title,author,cover,digest,source_url,content_url,post_time,create_time) ' \
              'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        return sql

# wx_list=[{'id':'MzI0MjA1Mjg2Ng==','name':'caoz的梦呓'}]
wx_list=[
         # {'id':'MjM5ODIyMTE0MA==','name':'小道消息'},
         # {'id':'MzI2OTM2NzA2OA==','name':'亦无所知'},
         {'id':'MzI2MzE2NDczMw==','name':'半佛仙人'},
         {'id':'MzIxODUxMDM5MQ==','name':'多元思维Hack'},
         # {'id':'MzI5MTE2NDI2OQ==','name':'仙人jump'},
        ]
if __name__ == '__main__':
    #
    for e in wx_list:
        wx_id=e['id']
        wx_name=e['name']
        savepath='./data/%s'%(wx_name)
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        biz = wx_id
        pass_ticket = 'tXyQ3SIhI20x4eTt1ff3nkKLtw1HfEHY7aJ819gkjaXWM0/+8Gq59ZT0yXvtnwc2'
        app_msg_token = '1024_mOYqBIXr4OCuvozhnfghgIl2yFZ4xk_6HweI3w~~'
        cookie = 'wap_sid2=CMXf+KgIEnA3QVdyRl9maldRaXVWM0YzRG5DOHpFS2JaOVJ5c052NFItNlk0WHFrcnMwTkIzbGoyU0J5NV9SMTQzSE9haUc2MUFDenJxNFJNS0FUQ2RaNmxWbTNsRzBpYWVhcHIxQjlBWkpMOU8wU08wY0FCQUFBMMmJuesFOA1AlU4='
        columns=['title','cover','author','digest','source_url','content_url','content_html']
        # 以上信息不同公众号每次抓取都需要借助抓包工具做修改
        wxMps = WxMps(biz, pass_ticket, app_msg_token, cookie,_offset=0,_savepath=savepath,_cols=columns)
        wxMps.start()  # 开始爬取文章
    # biz = 'MzI0MjA1Mjg2Ng=='
    # pass_ticket = '85YlQBaFkvkBu6FztelhJ/swBGVSAOdvUJGpA2RPway5KbP2TAcNeY/fmqyJSoXx'
    # app_msg_token = '1024_OA0LhyKVbqEkq4Fy73MQ9ZWmYfJ-H_n3YSxUbQ~~'
    # cookie = 'wap_sid2=CNS82qcIElxjN3FCQjdWZ2hEWjZ6bHlwUGM1YnhuckJ3ZzZJal9iZkloYk9UU2psM042VHM4bUdVZE9pVUozaEk5emc2eWhleVFOXzBmLVQtbE1qci1pdXZGQjlXd0FFQUFBfjD1na/rBTgNQJVO'
    # columns=['title','cover','author','digest','source_url','content_url']
    # # 以上信息不同公众号每次抓取都需要借助抓包工具做修改
    # wxMps = WxMps(biz, pass_ticket, app_msg_token, cookie,_offset=0,_savepath='.',_cols=columns)
    # wxMps.start()  # 开始爬取文章
