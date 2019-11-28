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
1、创建8个处理线程、一个清理字典的线程【清理】、告警线程
2、全局变量定义好每个线程需要处理的请求
3、期号判断 
'''
# 全局变量
data_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s'
# data_url ='%s/frommesg?__=frommesg&gameIndex=3&settlement=0&t=%s&beforeDate=%s&timesNum=%s&category_id=0'
query_data_set =set()
url=''
# 线程字典 {threadNo:{termNo:startPage:,endPage:,status:'0 没处理，1，已处理'}}
threadDic={}
# 告警字典
alarmDic={}
# 处理数据的id集合
data_ids = []
data_order_nos = set()
last_data_id=0
cur_last_data_id=0
# 当前期数
current_cicle = ''
# 期数集合
tips = set()
p = 1
s = Session()
t=''
threadNo=16
isNew=False
class pullDataThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        pullData(self.name)
        print("Exiting " + self.name)
def pullData(threadName):
    while True:
        try:
            if threadDic.get(threadName)!=None:
                if len(threadDic[threadName])==0:
                    continue
                l = threadDic[threadName]
                for e in l:
                    # if e.get('status') == 0:
                    # if e.get('termNo')== current_cicle:
                    termNo = e.get('termNo')
                    q_num  = e.get('q_num')
                    q_date = e.get('q_date')
                    pageListStr = e.get('pageList')
                    data_list = []
                    data_order_no_set1=set()
                    for p in str.split(pageListStr,'-'):
                        # p = i
                        # query_data_set.add('%s_%s_%s'%(str(p),str(q_date),str(q_num)))
                        # q_url=data_url % (str(url), str(p), str(t),str(q_date),str(q_num))
                        response = s.get(data_url % (str(url), str(p), str(t)))
                        jsonobj = json.loads(response.text)
                        if len(jsonobj['list'])==0:
                            continue
                        soup1 = BeautifulSoup(jsonobj['list'][0][0], "html.parser")
                        # 下单号 缺陷：一个单号多页，不能区别分没有下载的
                        # data_order_no_str=threadName + '_' + soup1.span.text
                        # if data_order_no_str in data_order_nos:
                        #     print(format_time(),'data_order_nos', threadName, soup1.span.text, data_order_nos)
                        #     break
                        # data_order_no_set1.add(data_order_no_str)
                        data_id1 = soup1.span.attrs["data-id"]
                        global  last_data_id
                        if isNew==False and int(last_data_id) == int(data_id1):
                            last_data_id=cur_last_data_id
                            sleep(5)
                            break
                        for e1 in jsonobj['list']:
                            code = e1[3]
                            money = e1[5]
                            soup = BeautifulSoup(e1[0], "html.parser")
                            data_id = soup.span.attrs["data-id"]
                            # data_order_no_set1.add(data_order_no_str)
                            # result.append('%s=%s,' % (str(code), str(money)))
                            if data_id not in data_ids:
                                # tip()
                                data_ids.append(data_id)
                                data_list.append('%s=%s' % (str(code), str(money)))
                                # print(format_time(), "新码:", threadName,p, data_id, code, money)
                    with open('D:/%s.txt' % (str(termNo)), 'a+', encoding='utf-8') as f:
                        if len(data_list) > 0:
                            f.write(',' + ','.join(data_list))
                            print(format_time(), threadName,'写入', len(data_list))
                        # e['status'] = 1
                        # threadDic[threadName]=[]
                    # for e in data_order_no_set1:
                    #     data_order_nos.add(e)
                    # print(format_time(), 'pullData-----1', threadDic)
            time.sleep(2)
        except Exception as e:
            print(format_time(), e)
            traceback.print_exc()
            time.sleep(5)
class alarmThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        dealAlarmData(alarmDic)
        print("Exiting " + self.name)

# 告警字典处理
def dealAlarmData(_alarmDic):
    while True:
        newAlarmDic={}
        print(format_time(), 'clearThreadData-----3', _alarmDic)
        for (k,v) in alarmDic.items():
            if v==0:
                print(format_time(), 'dealAlarmData-----0', _alarmDic)
                newAlarmDic[k]=v
                tip()
                v=1
                print(format_time(), 'dealAlarmData-----1', _alarmDic)
        _alarmDic=newAlarmDic
        time.sleep(5)

# 定时清理已处理的线程中的期数
class clearThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        clearThreadData(threadDic)
        print("Exiting " + self.name)

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

        # 创建8个处理线程
        global threadNo
        global threadDic
        for i in range(threadNo):
            threadDic["Thread-%s" % (str(i+1))]=[]
            pullDataThread(i + 1, "Thread-%s" % (str(i+1))).start()
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
        # driver_account.get(url)
        # driver_account.get()
        # driver_account.maximize_window()

        driver_account.get(url)
        # driver_account.find_element_by_id('search').send_keys(search_code)
        # sleep(1)
        # driver_account.find_element_by_id('btnSearch').click()
        # sleep(3)
        # driver_account.find_element_by_id('username').send_keys(username)
        # sleep(1)
        # driver_account.find_element_by_id('pass').send_keys(pwd)

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

                # data_url ='%s/frommesg?__=frommesg&gameIndex=%s&settlement=0&beforeDate=2019-11-01&timesNum=20191101016&category_id=0&t=%s'
                response = s.get(data_url % (str(url),str(p), str(t)))
                jsonobj = json.loads(response.text)
                totalPage = jsonobj['totalPage']
                q_date=jsonobj['dateAry'][0]
                q_num=jsonobj['numAry'][0]
                if len(jsonobj['list']) == 0:
                    sleep(5)
                    continue
                soup = BeautifulSoup(jsonobj['list'][0][0], "html.parser")
                soup2 = BeautifulSoup(jsonobj['list'][0][2], "html.parser")
                # 新的一期做处理  1、清理数据【ids】 2、告警数据处理
                global current_cicle
                global alarmDic
                global data_order_nos
                global isNew
                global cur_last_data_id
                # 不用单号判断，用date_id
                # if(soup.span.text in data_order_nos):
                #     sleep(5)
                #     continue
                global last_data_id
                cur_last_data_id=soup.span.attrs["data-id"]
                if current_cicle != soup2.span.text:
                    current_cicle = soup2.span.text
                    data_ids.clear()
                    if len(jsonobj['list'])>0:
                        # 告警处理
                        if current_cicle not in alarmDic.keys():
                            alarmDic[current_cicle]=0
                            tip()
                            last_data_id = soup.span.attrs["data-id"]
                            isNew = True
                else:
                    isNew=False

                for i in range(totalPage):
                    threadName="Thread-%s" % (str(i%threadNo+1))
                    # threadDic = {
                    #     'thread-1': [{'termNo': '2019110201', 'pageList': 1-3-5, 'status': '0'},
                    #                  {'termNo': '2019110202', 'pageList': [1, 3, 5], 'status': '0'}]}
                    if threadDic.get(threadName)!=None:
                        l = threadDic[threadName]
                        hasNo=False
                        for e in l:
                            if e.get('termNo')== current_cicle and e['status']==0:
                                hasNo=True
                                if str(i+1) not in str(e['pageList']).split('-'):
                                    e['pageList']=e['pageList']+'-'+str(i+1)
                        if hasNo==False:
                            newList=[]
                            e={}
                            e['termNo'] = current_cicle
                            e['status'] = 0
                            e['q_date'] = q_date
                            e['q_num'] = q_num
                            e['pageList'] = str(i + 1)
                            newList.append(e)
                            threadDic[threadName]=newList
                print(format_time(), 'threadDic',threadDic)
                print(format_time(), 'alarmDic',alarmDic)


                # list = jsonobj['list']
                # if len(list) >0 :
                #     tip()

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
