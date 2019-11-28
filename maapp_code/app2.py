#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we determine the event sender
object.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import time
import re
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from requests import Session
import json
from bs4 import BeautifulSoup
from pygame import mixer # Load the required library
import datetime
import base64
import traceback
import threading
import time
# 多线程
'''
1、根据数据创建线程数
2、期号+页数 判断是都处理过
3、期号判断 
'''
# 全局变量
data_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s'
url=''
# 线程字典 {threadNo:{termNo:startPage:,endPage:,status:'0 没处理，1，已处理'}}
threadDic={}
# 告警字典
alarmDic={}
# 处理数据的id集合
data_ids = []

# 当前期数
current_cicle = ''
# 期数集合
tips = set()
p = 1
s = Session()
t=''
threadNo=16
#期数+最后一页
termPageDic={}
class pullDataThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name,pageList,termNo):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pageList = pageList
        self.termNo = termNo

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        pullData(self.name,self.pageList,self.termNo)
        print("Exiting " + self.name)
def pullData(threadName,pageList,termNo):
    data_list=[]
    for p in pageList:
        # p = i
        response = s.get(data_url % (str(url), str(p), str(t)))
        jsonobj = json.loads(response.text)
        for e1 in jsonobj['list']:
            code = e1[3]
            money = e1[5]
            soup = BeautifulSoup(e1[0], "html.parser")
            data_id = soup.span.attrs["data-id"]
            # result.append('%s=%s,' % (str(code), str(money)))
            if data_id not in data_ids:
                # tip()
                data_ids.append(data_id)
                data_list.append('%s=%s' % (str(code), str(money)))
                # print(format_time(), "新码:", threadName,p, data_id, code, money)
        sleep(2)
    with open('D:/%s.txt' % (str(termNo)), 'a+', encoding='utf-8') as f:
        if len(data_list) > 0:
            f.write(',' + ','.join(data_list))

        # print("%s: %s" % (threadName, time.ctime(time.time())))

#             告警线程  定时告警

def clearThreadData(_threadDic):

    # threadDic={'thread-1':[{'termNo':'2019110201','startPage':'1','pageList':[1,3,5],'status':'0'},{'termNo':'2019110202','pageList':[1,3,5],'status':'0'}]}
    while True:
        newThreadDic = {}
        for (k, v) in _threadDic.items():
            newList = []
            for d in v:
                if d['status'] == '0':
                    print(format_time(),'threadDic',_threadDic)
                    newList.append(d)
            newThreadDic[k] = newList
        _threadDic=newThreadDic
        print(format_time(), 'clearThreadData-----1', _threadDic)
        time.sleep(60)


def getEndTime():
    with open(r'D:/app/conf.txt', encoding='utf-8') as fb:  ###被读者
        content = fb.readlines()
        decodestr= base64.b64decode(content[0].split(',')[1])
        endDateStr=decodestr.decode()
        print(format_time(), "************************************************到期时间为：", endDateStr)
    return endDateStr

def format_time():
    return "%s-%s-%s %s:%s:%s" % (
        time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
        time.localtime().tm_min, time.localtime().tm_sec)


def format_filename():
    return "%s%s%s%s%s%s" % (
        time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
        time.localtime().tm_min, time.localtime().tm_sec)
def tip():
    print(format_time(), '有新的下注码！！！！！')
    mixer.init()
    mixer.music.load('D:/app/tip.mp3')
    mixer.music.play()
    print(format_time(), '休息5秒')
    time.sleep(5)
def isTimeOut(endDateStr):

    end_time = int(datetime.datetime.strptime(endDateStr, '%Y-%m-%d').timestamp()) * 1000
    now_time = int(datetime.datetime.now().timestamp() * 1000)
    if now_time > end_time:
        print(format_time(),'该会员已到期,到期日期为：',endDateStr)
        return True
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        # tip()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton("begin", self)
        btn1.move(30, 50)


        btn1.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def genma(self):

        # print(format_time(), '************************************************到期日期为：', endDateStr)
        # url = 'http://ag1.aa9797.com' vip888 ok0006 bb123456
        # # url='http://ag1.td9898.com'#kkjj001 aa123456 vip666
        # search_code = '147147'
        # account = 'jk5599 '
        # pwd = 'aa123456'

        with open(r'D:/app/conf.txt', encoding='utf-8') as fb:  ###被读者
            content = fb.readlines()
            # print(format_time(), "配置信息",content[0])
        decodestr=content[0].split(',')[0]
        global url
        url = base64.b64decode(decodestr).decode()


        # for i in range(threadNo):
        #     threadDic["Thread-%s" % (str(i+1))]=[]
        #     pullDataThread(i + 1, "Thread-%s" % (str(i+1))).start()
        # alarmThread(1, "AlarmThread").start()
        # clearThread(1, "clearThread").start()
        endDateStr = getEndTime()
        if isTimeOut(endDateStr) == True:
            exit()
        print(format_time(),'代理网址为：',url)
        # search_code=content[0].split(',')[1]
        # username=content[0].split(',')[2]
        # pwd=content[0].split(',')[3]
        webdriver.ChromeOptions.binary_location = 'D:/app/chrome/chrome.exe'
        """会员登录 start"""
        driver_account = webdriver.Chrome('D:/app/chromedriver.exe')


        driver_account.get(url)

        """会员登录 end"""
        print(format_time(), "一分钟内快速登录！！！！！")
        sleep(40)
        # while True:
        #     wait.until(EC.presence_of_element_located((By.ID, 'shell_title')))
        #     if driver_account.find_element_by_xpath('//*[@id="shell_title"]').text == '最新公告':
        #         print(format_time(), "会员登录成功")
        #         break
        #     sleep(5)


        # Reddit will think we are a bot if we have the wrong user agent
        selenium_user_agent = driver_account.execute_script("return navigator.userAgent;")
        s.headers.update({"user-agent": selenium_user_agent})
        for cookie in driver_account.get_cookies():
            s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        global  t
        t= driver_account.page_source.split('autoTid')[1].split(':')[1].split(',')[0].replace('\\', '').replace('"','')

        print(format_time(), "t:", t)
        while True:
            try:
                #
                # data_url ='%s/frommesg?__=frommesg&gameIndex=%s&settlement=0&beforeDate=2019-11-01&timesNum=20191101016&category_id=0&t=%s'
                response = s.get(data_url % (str(url),str(p), str(t)))
                jsonobj = json.loads(response.text)
                totalPage = jsonobj['totalPage']
                # global threadNo
                # for i in range(threadNo):
                #     # threadDic["Thread-%s" % (str(i + 1))] = []
                #     pageList=[]
                #     pullDataThread(i + 1, "Thread-%s" % (str(i + 1)),).start()
                if len(jsonobj['list']) == 0:
                    sleep(5)
                    continue
                soup2 = BeautifulSoup(jsonobj['list'][0][2], "html.parser")
                # 新的一期做处理  1、清理数据【ids】 2、告警数据处理
                global current_cicle
                global alarmDic
                if current_cicle != soup2.span.text:
                    current_cicle = soup2.span.text
                    data_ids.clear()

                    if len(jsonobj['list'])>0:
                        # 告警处理
                        if current_cicle not in alarmDic.keys():
                            alarmDic[current_cicle]=0
                            tip()
                cachLastPage=1
                if current_cicle in termPageDic.keys():
                    cachLastPage=termPageDic.get(current_cicle)
                for i in range(cachLastPage,totalPage+1,threadNo):
                    startPage=i
                    endPage=i+threadNo
                    if endPage >= totalPage+1:
                        endPage = totalPage+1
                    pageList=[]
                    for j in range(startPage,endPage):
                        pageList.append(j)

                    threadName="Thread-[%s-%s]" % (str(startPage),str(endPage))
                    # threadDic = {
                    #     'thread-1': [{'termNo': '2019110201', 'pageList': 1-3-5, 'status': '0'},
                    #                  {'termNo': '2019110202', 'pageList': [1, 3, 5], 'status': '0'}]}
                    pullDataThread(i,threadName,pageList,current_cicle).start()

                print(format_time(), current_cicle,"休息5s!!!!")
                time.sleep(5)
            except Exception as e:
                print(format_time(), "异常重来:",e)
                traceback.print_exc()
                time.sleep(5)
                # driver_account.refresh()
                # self.genma()
            # with open('D:/app/%s.log' % (str(int(time.strftime('%Y%m%d')))), 'a',
            #           encoding='utf-8') as f:
            #     f.write(log_str + "\n")
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        self.genma()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
