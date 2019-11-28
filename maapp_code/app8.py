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

# 全局变量
data_url = '%s/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s'
data_url = '%s/frommesg?__=frommesg&gameIndex=3&settlement=4&beforeDate=2019-11-05&timesNum=20191105285&category_id=0&t=F54207C245C68CC031595D03D1461778'
url=''
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
        endDateStr=getEndTime()
        if isTimeOut(endDateStr)==True:
            exit()
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
        # wait = WebDriverWait(driver_account, 10)  # 等待
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
        sleep(60)
        # while True:
        #     wait.until(EC.presence_of_element_located((By.ID, 'shell_title')))
        #     if driver_account.find_element_by_xpath('//*[@id="shell_title"]').text == '最新公告':
        #         print(format_time(), "会员登录成功")
        #         break
        #     sleep(5)

        s = Session()
        # Reddit will think we are a bot if we have the wrong user agent
        selenium_user_agent = driver_account.execute_script("return navigator.userAgent;")
        s.headers.update({"user-agent": selenium_user_agent})
        for cookie in driver_account.get_cookies():
            s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        t = driver_account.page_source.split('autoTid')[1].split(':')[1].split(',')[0].replace('\\', '').replace('"','')
        p = 1
        print(format_time(), "t:", t)
        data_ids=[]
        data_list=[]
        current_cicle=''
        tips=set()
        while True:
            try:
                global data_url

                # data_url ='%s/frommesg?__=frommesg&gameIndex=%s&settlement=0&beforeDate=2019-11-01&timesNum=20191101016&category_id=0&t=%s'
                response = s.get(data_url % (str(url),str(p), str(t)))
                jsonobj = json.loads(response.text)
                totalPage = jsonobj['totalPage']
                # list = jsonobj['list']
                # if len(list) >0 :
                #     tip()
                for e in jsonobj['list']:
                    code = e[3]
                    money = e[5]
                    soup = BeautifulSoup(e[0], "html.parser")
                    data_id = soup.span.attrs["data-id"]
                    soup2 = BeautifulSoup(e[2], "html.parser")
                    if current_cicle != soup2.span.text:
                        print(format_time(), '本期号码：', current_cicle, ','.join(data_ids), '下注详情', ','.join(data_list))
                        data_ids.clear()
                        data_list.clear()
                        current_cicle = soup2.span.text
                        print(format_time(), '清理后：', current_cicle, ','.join(data_ids), '下注详情', ','.join(data_list))
                    # result.append('%s=%s,'%(str(code),str(money)))
                    if data_id not in data_ids:
                        if current_cicle not in tips:
                            tip()
                            tips.add(current_cicle)
                        # tip()
                        data_ids.append(data_id)
                        data_list.append('%s=%s'%(str(code),str(money)))
                        print(format_time(), "新码:", p, data_id, code, money)
                # print(jsonobj['list'])
                # print(len(jsonobj['list']))
                if totalPage > 1:
                    for i in range(2, totalPage + 1):
                        p = i
                        response = s.get(data_url % (str(url),str(p), str(t)))
                        jsonobj = json.loads(response.text)
                        for e in jsonobj['list']:
                            code = e[3]
                            money = e[5]
                            soup = BeautifulSoup(e[0], "html.parser")
                            data_id = soup.span.attrs["data-id"]
                            soup2 = BeautifulSoup(e[2], "html.parser")
                            if current_cicle != soup2.span.text:
                                print(format_time(), '本期号码：', current_cicle, ','.join(data_ids), '下注详情', ','.join(data_list))
                                data_ids.clear()
                                data_list.clear()
                                current_cicle = soup2.span.text
                                print(format_time(), '清理后：', current_cicle, ','.join(data_ids), '下注详情', ','.join(data_list))
                            # result.append('%s=%s,' % (str(code), str(money)))
                            if data_id not in data_ids:
                                if current_cicle not in tips:
                                    tip()
                                    tips.add(current_cicle)
                                # tip()
                                data_ids.append(data_id)
                                data_list.append('%s=%s' % (str(code), str(money)))
                                print(format_time(), "新码:", p, data_id, code, money)
                with open('D:/%s.txt'%(str(current_cicle)), 'a+', encoding='utf-8') as f:
                    if len(data_list) >0 :
                        f.write(','+','.join(data_list))
                        data_list.clear()

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
