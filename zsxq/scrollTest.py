from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import time
import re
from selenium.common.exceptions import TimeoutException

webdriver.ChromeOptions.binary_location = './App/chrome.exe'
driver_zsxq = webdriver.Chrome('chromedriver1.exe')
"""代理登录"""
driver_zsxq.get("https://blog.csdn.net/wumxiaozhu/article/details/81351828")
driver_zsxq.maximize_window()
wait = WebDriverWait(driver_zsxq, 30)  # 等待
from selenium import webdriver
import time
driver_zsxq.execute_script("window.scrollBy(0,3000)")
time.sleep(1)
driver_zsxq.execute_script("window.scrollBy(0,5000)")
time.sleep(1)
driver_zsxq.execute_script("window.scrollBy(0,8000)")
time.sleep(1)