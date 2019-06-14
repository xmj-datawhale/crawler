#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/14 9:56
@Author  : xumj
'''

import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# browser = webdriver.Chrome('chromedriver.exe')  # 声明一个浏览器对象
browser = webdriver.Chrome("D:\\360安全浏览器下载\\chromedriver_win32\\chromedriver.exe")
try:
    browser.get("https://time.geekbang.org/")  # 传入URL
    print(time.localtime())
finally:
    browser.close()