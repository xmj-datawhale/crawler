from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
'''跟注'''
webdriver.ChromeOptions.binary_location='./App/chrome.exe'

url='https://wx.qq.com/'
nickname='星期八-6994'
"""会员登录"""
driver_account = webdriver.Chrome('chromedriver1.exe')
driver_account.get(url)
driver_account.maximize_window()
wait=WebDriverWait(driver_account,10)#等待
wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div[1]/div[2]/h3/a/i')))
sleep(3)
cur_e=None
msgId_set=set()
for i in range(2,len(driver_account.find_elements_by_xpath('//*[@id="J_NavChatScrollBody"]/div/div[*]'))+1):
    e=driver_account.find_elements_by_xpath('//*[@id="J_NavChatScrollBody"]/div/div[%s]/div/div[3]/h3/span'%(str(i)))[0]
    if nickname==e.text :
        print(e.text)
        e.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chatArea"]/div[1]/div[2]/div/a')))
        while True:
            if driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[1]/div[2]/div/a')[0].text==nickname:
                break
            sleep(1)
        for i in (1,range(driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[*]').__len__()+1)):
            if driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[%s]'%(str(i))).__len__()>0:
                msg_text=driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[%s]'%(str(i)))[0].text
                if len(driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[%s]/div/div/div/div/div'%(str(i))))>0:
                    msgId=json.loads(driver_account.find_elements_by_xpath('//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[%s]/div/div/div/div/div'%(str(i)))[0].get_attribute('data-cm'))['msgId']
                print(msgId,msg_text)
        break





