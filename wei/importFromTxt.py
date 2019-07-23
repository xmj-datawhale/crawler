from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import time
import re
import numpy as np
import os
def format_time():
    return "%s-%s-%s %s:%s:%s" % (
    time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
    time.localtime().tm_min, time.localtime().tm_sec)
def format_filename():
    return "%s%s%s%s%s%s" % (
    time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
    time.localtime().tm_min, time.localtime().tm_sec)
'''跟注'''
# driver = webdriver.Chrome('E:\\workspace\\pyProjects\\apps\\chaobin\\selenium\\chromedriver.exe')
# webdriver.ChromeOptions.binary_location='D:\\Chrome_X64_75.0.3770.90\\App\\chrome.exe'
login_time=time.time()
url='http://m8989.net/'
proxy_input_no='668899'
# pwd='wei@123456'
pwd='aa0123456'
# account='ss889'
# search_account='ss668'
# my_account='ss868'
account='yyy88888'
search_account='ss668'
# my_account='yy5577'
my_account='yy66999'
webdriver.ChromeOptions.binary_location='./App/chrome.exe'

"""会员登录 start"""
driver_account = webdriver.Chrome('chromedriver1.exe')
# driver_account.get(url)
# driver_account.maximize_window()
wait1=WebDriverWait(driver_account,10)#等待
def account_login():
    driver_account.get(url)
    wait1.until(EC.presence_of_element_located((By.ID,'passcode')))
    driver_account.find_element_by_xpath('//*[@id="passcode"]').send_keys(proxy_input_no)
    driver_account.find_element_by_xpath('//*[@id="submitbtn"]').click()
    """选择会员线路"""
    account_road=random.randint(9,16)
    print(format_time(),"选择会员线路%s" % str(account_road))
    wait1.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[2]/a[{}]'.format(account_road))))
    href=driver_account.find_element(By.XPATH,'/html/body/div/div[2]/a[{}]'.format(account_road)).get_attribute('href')
    driver_account.get(href)

    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Account"]')))
    print(format_time(),"会员帐号", my_account, "pwd:", pwd)
    driver_account.find_element(By.XPATH,'//*[@id="Account"]').send_keys(my_account)
    driver_account.find_element(By.XPATH,'//*[@id="Password"]').send_keys(pwd)
    driver_account.find_element(By.XPATH,'//*[@id="btn-submit"]').click()
    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="agree"]')))
    sleep(4)
    while True:
        if driver_account.find_element_by_xpath('//*[@id="agree"]').get_attribute('value')=='同意':
            driver_account.find_element(By.XPATH, '//*[@id="agree"]').click()
            return True
            break
        sleep(1)

try:
    while True:
        if account_login():
            break
except:
    print(format_time(),"会员登录失败")
    sleep(3)
    account_login()
else:
    print(format_time(),"会员登录成功")
    sleep(3)
    print(format_time(),my_account,"余额",driver_account.find_elements(By.XPATH, '//*[@id="Cash"]')[0].text)
"""会员登录 end"""


"""以下注的单号"""
downed_order_no_list=[]
downed_terms=[]
while True:
    try:
        wait1.until(EC.presence_of_element_located((By.XPATH, '//*[@id ="showGameNum"]')))
        term_no = driver_account.find_elements(By.XPATH, '//*[@id ="showGameNum"]')[0].text
        # term_no = '50598867'
        code_path=os.path.join('./importtxt','%s.txt'%(term_no))
        if os.path.exists(code_path)==False:
            sleep(2)
            continue
        if term_no in downed_terms:
            sleep(2)
            continue
        if len(driver_account.find_elements(By.XPATH, '//*[@id="main"]/div/div/div/table/tbody/tr/td/div')) > 0 \
                and driver_account.find_elements(By.XPATH, '//*[@id="main"]/div/div/div/table/tbody/tr/td/div')[0].text == '已封盘':
            print(format_time(), term_no,"已封盘,未能下注")
            continue
        if len(downed_terms) >=100:
            print(format_time(), term_no,"已下注期数%d,现在清理"%(len(downed_terms)))
            downed_terms.clear()
        import_start=time.time()
        print(format_time(), my_account, term_no, "下注开始")
        """txt导入"""
        wait1.until(EC.presence_of_element_located((By.XPATH, '//*[@id="importtxt"]')))
        driver_account.find_elements(By.XPATH, '//*[@id="importtxt"]')[0].click()

        wait1.until(EC.presence_of_element_located((By.XPATH, '//*[@id="uploadForm"]/table/tbody/tr[1]/td[2]/input')))
        driver_account.find_elements(By.XPATH, '//*[@id="uploadForm"]/table/tbody/tr[1]/td[2]/input')[0].send_keys(os.path.abspath(code_path))
        wait1.until(EC.presence_of_element_located((By.XPATH, '//*[@id="uploadForm"]/table/tbody/tr[1]/td[3]/input')))
        driver_account.find_elements(By.XPATH, '//*[@id="uploadForm"]/table/tbody/tr[1]/td[3]/input')[0].click()
        wait1.until(EC.presence_of_element_located((By.XPATH, '//*[@id="order_submit"]')))
        driver_account.find_elements(By.XPATH, '//*[@id="order_submit"]')[0].click()
        Alert(driver_account).accept()
        sleep(1)
        print(format_time(),my_account,term_no,"下注完成,耗时%.2f\n"%(time.time()-import_start))
        downed_terms.append(term_no)
    # '//*[@id="importtxt"]'
    # '//*[@id="uploadForm"]/table/tbody/tr[1]/td[2]/input' //*[@id="uploadForm"]/table/tbody/tr[1]/td[3]/input
    except Exception as e:
        print(format_time(),term_no,e)