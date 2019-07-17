from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import random
def format_time():
    return "%s-%s-%s %s:%s:%s" % (
    time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
    time.localtime().tm_min, time.localtime().tm_sec)

'''跟注'''
webdriver.ChromeOptions.binary_location='./App/chrome.exe'

url='http://m8989.net/'
proxy_input_no='668899'
account='ss889'
pwd='wei@123456'
search_account='ss668'
my_account='ss868'
"""会员登录"""
driver_account = webdriver.Chrome('chromedriver1.exe')
driver_account.get(url)
driver_account.maximize_window()
wait1=WebDriverWait(driver_account,10)#等待
wait1.until(EC.presence_of_element_located((By.ID,'passcode')))
driver_account.find_element_by_xpath('//*[@id="passcode"]').send_keys(proxy_input_no)
driver_account.find_element_by_xpath('//*[@id="submitbtn"]').click()
wait1.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[2]/a[9]')))
href=driver_account.find_element(By.XPATH,'/html/body/div/div[2]/a[9]').get_attribute('href')
driver_account.get(href)
wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Account"]')))
driver_account.find_element(By.XPATH,'//*[@id="Account"]').send_keys(search_account)
driver_account.find_element(By.XPATH,'//*[@id="Password"]').send_keys(pwd)
driver_account.find_element(By.XPATH,'//*[@id="btn-submit"]').click()
sleep(6)
wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="agree"]')))
while True:
    if driver_account.find_element(By.XPATH, '//*[@id="agree"]').get_attribute('value')=='同意':
        break
    sleep(1)
driver_account.find_element(By.XPATH,'//*[@id="agree"]').click()

"""下注"""

down_gold=1
"""已封盘"""
while True:
    down_code = '%d%d%d%d' % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    if len(driver_account.find_elements(By.XPATH,'//*[@id="main"]/div/div/div/table/tbody/tr/td/div')) >0 \
            and driver_account.find_elements(By.XPATH, '//*[@id="main"]/div/div/div/table/tbody/tr/td/div')[0].text=='已封盘':
        sleep(10)
        continue
    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="NumType"]')))
    driver_account.find_element(By.XPATH,'//*[@id="NumType"]').click()
    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="number"]')))
    driver_account.find_element(By.XPATH,'//*[@id="number"]').send_keys(down_code)
    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="gold"]')))
    driver_account.find_element(By.XPATH,'//*[@id="gold"]').send_keys(down_gold)
    wait1.until(EC.presence_of_element_located((By.XPATH,'//*[@id="kuaida"]')))
    driver_account.find_element(By.XPATH,'//*[@id="kuaida"]/div[2]/div/table[2]/tbody/tr/td[3]/input[1]').click()
    print(format_time(),down_code,down_gold)
    sleep(90)
print(8)

