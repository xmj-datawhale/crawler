#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
多线程写入
使用归档查询
配置文件数据说明：文件路径，线程数，登录超时，拉取数据总数
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
import os, stat
from queue import Queue
import math
# deskPath=os.path.join(os.path.expanduser('~'), "Desktop")
# deskPath='D:/app'


# 多线程
'''
1、创建8个处理线程、一个清理字典的线程【清理】、告警线程
2、全局变量定义好每个线程需要处理的请求
3、期号判断 
'''

class VarClazz():
    # 全局变量
    data_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s'
    guidang_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s&settlement=4&category_id=0'
    # guidang_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s&settlement=4&category_id=0&beforeDate=2019-11-28&timesNum=20191128138'
    url = ''
    # 线程字典 {threadNo:{termNo:startPage:,endPage:,status:'0 没处理，1，已处理'}}
    threadDic = {}
    alarmDic = {}
    # 当前期数
    current_cicle = ''
    p = 1
    s = Session()
    t = ''
    order_num = 0
    max_data_id = 0
    # 新数据标志 当所有线程拉数完毕时设置为False
    newDataFlag = False
    countList = []
    codeDic = {}
    # 配置文件数据
    deskPath = 'C:\\Users\\Administrator\\Desktop'  # 数据文件路径 配置文件 index=0
    threadNo = 5  # 线程数 配置文件 index=1
    totalNo = 30000  # 数据总数 配置文件 index=2
    loginTimeOut = 30  # 登录超时 配置文件 index=3
    lastTotalPage = 1
    endPageNo = 1
if os.path.exists(os.path.join('D:/app', 'other_conf.txt')):
    with open(os.path.join('D:/app', 'other_conf.txt'),'r',encoding='utf-8') as f:
        other_confs=str.strip(f.read())
        path_cxt=other_confs.split(',')[0]
        if(path_cxt!=None):
            if not os.path.exists(path_cxt):
                os.mkdir(path_cxt)
            VarClazz.deskPath=path_cxt
        if len(other_confs.split(','))>=2:
            VarClazz.threadNo=int(other_confs.split(',')[1])
        if len(other_confs.split(','))>=3:
            VarClazz.totalNo=int(other_confs.split(',')[2])
        if len(other_confs.split(','))>=4:
            VarClazz.loginTimeOut=int(other_confs.split(',')[3])
print('写入目录是：', VarClazz.deskPath,'线程数：',VarClazz.threadNo)

# 线程分类
# data_list = []  # 任四
# data_list1 = []  # 任一
# data_list2 = []  # 任二
# data_list3 = []  # 任三
# data_list5 = []  # 任五
# data_list_all = []  # 注单
class pullDataThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name,driver_account):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.driver_account = driver_account

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        pullData(self.name,self.threadID,self.driver_account)
        print("Exiting " + self.name)
def pullData(threadName,threadID,driver_account):
    while True:
        try:
            #
            if VarClazz.threadDic[threadName]['status']==1:
                print(format_time(), threadName,'启动！！！！')
                data_list = []  # 任四
                data_list1 = []  # 任一
                data_list2 = []  # 任二
                data_list3 = []  # 任三
                data_list5 = []  # 任五
                data_list_all = []  #
                totalCount=0
                for p in range(threadID,int(VarClazz.totalNo/20),VarClazz.threadNo):
                    # response = s.get(guidang_url % (str(url), str(p), str(t)))
                    response = VarClazz.s.get(VarClazz.data_url % (str(VarClazz.url), str(p), str(VarClazz.t)))
                    jsonobj = json.loads(response.text)
                    _dataList=jsonobj['list']
                    print(format_time(),threadName,'page:',p,'len:',len(_dataList))
                    if len(_dataList)==0:
                        VarClazz.countList.append(totalCount)
                        break
                    totalCount=+len(_dataList)
                    # print(format_time(),'pullData',_dataList[0:2])
                    for e1 in _dataList:
                        code = e1[3]
                        money = e1[5]
                        soup = BeautifulSoup(e1[0], "html.parser")
                        data_id = soup.span.attrs["data-id"]

                        if str(code).find('球') != -1:
                            # print(code[1])
                            # print(code.split('>')[1].split('<')[0])
                            code0 = code.split('>')[1].split('<')[0]
                            dic = {'一': '%sXXX', '二': 'X%XX', '三': 'XX%sX', '四': 'XXX%s', '五': 'XXXX%s'}
                            codeIndex = code[1]
                            code = dic[codeIndex] % (str(code0))
                        type_num = len([i for i in range(len(code)) if str.upper(code[i]) != 'X'])
                        # if VarClazz.codeDic.get(data_id):
                        #     continue
                        # else:
                        #     VarClazz.codeDic[data_id] = '%s=%s' % (str(code), str(money))
                        if type_num == 1 :  # 任一
                            data_list1.append('%s=%s' % (str(code), str(money)))
                        elif type_num == 3:  # 任三
                            data_list3.append('%s=%s' % (str(code), str(money)))
                        elif type_num == 2:  # 任二
                            data_list2.append('%s=%s' % (str(code), str(money)))
                        elif type_num == 4:  # 任四
                            data_list.append('%s=%s' % (str(code), str(money)))
                        elif type_num == 5:  # 任五
                            data_list5.append('%s=%s' % (str(code), str(money)))
                        data_list_all.append('%s=%s' % (str(code), str(money)))
                with open(os.path.join(VarClazz.deskPath, '注单.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list_all) > 0:
                        f.write(',' + ','.join(data_list_all))
                        order_num = +len(data_list)
                        print(format_time(), threadName, '注单写入', len(data_list))
                with open(os.path.join(VarClazz.deskPath, '任五.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list5) > 0:
                        f.write(',' + ','.join(data_list5))
                        print(format_time(), threadName, '任五写入', len(data_list5))
                with open(os.path.join(VarClazz.deskPath, '任四.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list) > 0:
                        f.write(',' + ','.join(data_list))
                        print(format_time(), threadName, '任四写入', len(data_list))
                with open(os.path.join(VarClazz.deskPath, '任三.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list3) > 0:
                        f.write(',' + ','.join(data_list3))
                        print(format_time(), threadName, '任三写入', len(data_list3))
                with open(os.path.join(VarClazz.deskPath, '任二.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list2) > 0:
                        f.write(',' + ','.join(data_list2))
                        print(format_time(), threadName, '任二写入', len(data_list2))
                with open(os.path.join(VarClazz.deskPath, '任一.txt'), 'a+', encoding='utf-8') as f:
                    if len(data_list1) > 0:
                        f.write(',' + ','.join(data_list1))
                        print(format_time(), threadName, '任一写入', len(data_list1))
                VarClazz.threadDic[threadName] = {'status': 0}
                print(format_time(), threadName, '数据拉去完毕！！！')
            time.sleep(2)
        except Exception as e:
            print(format_time(), "pullData:", e)
            traceback.print_exc()
            time.sleep(5)
        # print("%s: %s" % (threadName, time.ctime(time.time())))

def getNameByType(gameIndex,type) :
    if gameIndex == 3:
        if type >= 1 and type <= 10:
            tmp=(type-1)
            return str(tmp) + "XXXX"
        elif type >= 15 and type <= 24:
            tmp = (type-15)
            return "X" + (type-15) + "XXX"
        elif type >= 29 and type <= 38:
            tmp = (type - 29)
            return "XX" + str(tmp) + "XX"
        elif type >= 43 and type <= 52:
            tmp = (type - 43)
            return "XXX" + str(tmp) + "X"
        elif type >= 57 and type <= 66:
            tmp = (type - 57)
            return "XXXX" + str(tmp)
        elif type >= 108 and type <61108:
            return getDwNameByType(type)
def getDwNameByType(type):
    # str(math.floor(type / 10))
    if type < 208 :# 萬千XXX
        type -= 108
        return str(math.floor(type / 10)) + str((str(type % 10))) + "XXX"
    elif type < 308 :# 萬X百XX
        type -= 208
        return str(math.floor(type / 10)) + "X" + (str(type % 10)) + "XX"
    elif type < 408 :# 萬XX十X
        type -= 308
        return str(math.floor(type / 10)) + "XX" + str(type % 10) + "X"
    elif type < 508 :# 萬XXX个
        type -= 408
        return str(math.floor(type / 10)) + "XXX" + (str(type % 10))
    elif type < 608 :# X千百XX
        type -= 508
        return "X" + str(math.floor(type / 10)) + str((str(type % 10))) + "XX"
    elif type < 708 :# X千X十X
        type -= 608
        return "X" + str(math.floor(type / 10)) + "X" + (str(type % 10)) + "X"
    elif type < 808 :# X千XX个
        type -= 708
        return "X" + str(math.floor(type / 10)) + "XX" + (str(type % 10))
    elif type < 908 :# XX百十X
        type -= 808
        return "XX" + str(math.floor(type / 10)) + (str(type % 10)) + "X"
    elif type < 1008 :# XX百X个
        type -= 908
        return "XX" + str(math.floor(type / 10)) + "X" + (str(type % 10))
    elif type < 1108 :# XXX十个
        type -= 1008
        return "XXX" + str(math.floor(type / 10)) + (str(type % 10))
    elif type < 2108:  # 万千百XX
        type -= 1108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "XX"
    elif type < 3108:  # 万千X十X
        type -= 2108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10) + "X"
    elif type < 4108:  # 万千XX个
        type -= 3108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "XX" + (type % 100 % 10)
    elif type < 5108:  # 万X百十X
        type -= 4108
        return str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "X"
    elif type < 6108:  # 万X百X个
        type -= 5108
        return str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10)
    elif type < 7108:  # 万XX十个
        type -= 6108
        return str(math.floor(type / 100)) + "XX" + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 8108:  # X千百十X
        type -= 7108
        return "X" + str(math.floor(type / 100)) + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "X"
    elif type < 9108:  # X千百X个
        type -= 8108
        return "X" + str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10)
    elif type < 10108:  # X千X十个
        type -= 9108
        return "X" + str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 11108:  # XX百十个
        type -= 10108
        return "XX" + str(math.floor(type / 100)) + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 21108:  # 万千百十X
        type -= 11108
        return str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10)) + "X"
    elif type < 31108:  # 万千百X个
        type -= 21108
        return str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + "X" + str(math.floor(type % 1000 % 100 % 10))
    elif type < 41108:  # 万千X十个
        type -= 31108
        return str(math.floor(type / 1000)) + str(math.floor(type % 1000 / 100)) + "X" + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))
    elif type < 51108:  # 万X百十个
        type -= 41108
        return str(math.floor(type / 1000)) + "X" + str(math.floor(type % 1000 / 100)) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))
    elif type < 61108:  # X千百十个
        type -= 51108
        return "X" + str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))

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
def defFiles():
    print(format_time(),VarClazz.deskPath,'清空该目录文件')
    if os.path.exists(os.path.join(VarClazz.deskPath, '注单.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '注单.txt'))
    if os.path.exists(os.path.join(VarClazz.deskPath, '任五.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '任五.txt'))
    if os.path.exists(os.path.join(VarClazz.deskPath, '任四.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '任四.txt'))
    if os.path.exists(os.path.join(VarClazz.deskPath, '任三.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '任三.txt'))
    if os.path.exists(os.path.join(VarClazz.deskPath, '任二.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '任二.txt'))
    if os.path.exists(os.path.join(VarClazz.deskPath, '任一.txt')):
        os.remove(os.path.join(VarClazz.deskPath, '任一.txt'))
# 设置线程状态 0没有数据，1 有数据
def setThreadStatus(threadDic,status):
    if status==1:
        for key in threadDic.keys():
            while threadDic[key]['status']==0:
                threadDic[key]['status'] = 1
                sleep(0.1)
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
        VarClazz.url = base64.b64decode(decodestr).decode()

        # 创建8个处理线程
        # global threadNo
        # global threadDic
        # global current_cicle
        # global alarmDic
        # global max_data_id
        # global order_num
        # global newDataFlag
        # global loginTimeOut
        # global lastTotalPage
        # global endPageNo
        # global codeDic
        # alarmThread(1, "AlarmThread").start()
        # clearThread(1, "clearThread").start()
        endDateStr = getEndTime()
        if isTimeOut(endDateStr) == True:
            exit()
        print(format_time(),'代理网址为：',VarClazz.url)
        # search_code=content[0].split(',')[1]
        # username=content[0].split(',')[2]
        # pwd=content[0].split(',')[3]
        webdriver.ChromeOptions.binary_location = 'D:/app/chrome/chrome.exe'
        """会员登录 start"""
        driver_account = webdriver.Chrome('D:/app/chromedriver.exe')
        # driver_account.get(url)
        # driver_account.get()
        # driver_account.maximize_window()

        driver_account.get(VarClazz.url)
        for i in range(VarClazz.threadNo):
            VarClazz.threadDic["Thread-%s" % (str(i+1))]={'status':0}
            pullDataThread(i + 1, "Thread-%s" % (str(i+1)),driver_account).start()
        # checkDataStatusThread( 1, "checkDataStatusThread").start()


        """会员登录 end"""
        print(format_time(), "一分钟内快速登录！！！！！")
        sleep(VarClazz.loginTimeOut)
        # Reddit will think we are a bot if we have the wrong user agent
        selenium_user_agent = driver_account.execute_script("return navigator.userAgent;")
        VarClazz.s.headers.update({"user-agent": selenium_user_agent})
        for cookie in driver_account.get_cookies():
            VarClazz.s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        while True:
            if driver_account.page_source.split('autoTid'):
                break
            sleep(5)
        VarClazz.t= driver_account.page_source.split('autoTid')[1].split(':')[1].split(',')[0].replace('\\', '').replace('"','')
        print(format_time(), "t:", VarClazz.t)

        while True:
            try:
                # data_url ='%s/frommesg?__=frommesg&gameIndex=%s&settlement=0&beforeDate=2019-11-01&timesNum=20191101016&category_id=0&t=%s'
                response = VarClazz.s.get(VarClazz.data_url % (str(VarClazz.url),str(VarClazz.p), str(VarClazz.t)))
                jsonobj = json.loads(response.text)

                # 新的一期做处理  1、清理数据【ids】 2、告警数据处理
                cur_max_data_id=0
                if (len(jsonobj['list']) > 0):
                    cur_max_data_id = BeautifulSoup(jsonobj['list'][0][0], "html.parser").span.attrs['data-id']
                if VarClazz.current_cicle != jsonobj['numAry'][0]:#新的一期处理
                    VarClazz.max_data_id=0

                    if len(jsonobj['list'])>0:#有数据
                        VarClazz.current_cicle = jsonobj['numAry'][0]
                        # 告警处理
                        if VarClazz.current_cicle not in VarClazz.alarmDic.keys():
                            VarClazz.codeDic={}
                            VarClazz.alarmDic[VarClazz.current_cicle]=0
                            defFiles()
                            setThreadStatus(VarClazz.threadDic, 1)
                            tip()
                    else:
                        sleep(5)
                        continue
                else:#同一期处理
                    if(int(cur_max_data_id)==int(VarClazz.max_data_id)):
                        sleep(2)
                        continue
                    else:
                        if(cur_max_data_id!=0):
                            # 新数据标识
                            # newDataFlag = True
                            # setThreadStatus(threadDic, 0)
                            # order_num=0
                            # defFiles()
                            VarClazz.max_data_id=cur_max_data_id
                            setThreadStatus(VarClazz.threadDic, 1)
                            sleep(2)
                print(format_time(), VarClazz.current_cicle,"休息5s!!!!")
                time.sleep(5)
            except Exception as e:
                print(format_time(),e)
                # traceback.print_exc()
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
