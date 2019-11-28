from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import time
from requests import Session
import json
from bs4 import BeautifulSoup
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
url='http://ag1.kk688688.com'
# url='http://ag1.td9898.com'#kkjj001 aa123456 vip666
search_code='147147'
account='jk5599'
pwd='aa123456'
webdriver.ChromeOptions.binary_location='./App/chrome.exe'

"""会员登录 start"""
driver_account = webdriver.Chrome('chromedriver1.exe')
# driver_account.get(url)
# driver_account.maximize_window()
wait=WebDriverWait(driver_account,10)#等待
driver_account.get(url)
"""会员登录 end"""
sleep(40)
while True:
    wait.until(EC.presence_of_element_located((By.ID, 'shell_title')))
    if driver_account.find_element_by_xpath('//*[@id="shell_title"]').text=='最新公告':
        print(format_time(), "会员登录成功")
        break
    sleep(5)


s = Session()
# Reddit will think we are a bot if we have the wrong user agent
selenium_user_agent = driver_account.execute_script("return navigator.userAgent;")
s.headers.update({"user-agent": selenium_user_agent})
for cookie in driver_account.get_cookies():
    s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
t=driver_account.page_source.split('autoTid')[1].split(':')[1].split(',')[0].replace('\\','').replace('"','')
p=1
print(format_time(), "t:",t)
# data_url='http://ag1.kk688688.com/frommesg?__=frommesg&gameIndex=3&page=%s&t=%s'
data_url='http://ag1.kk688688.com/frommesg?__=frommesg&gameIndex=3&settlement=0&beforeDate=2019-10-28&timesNum=20191028003&category_id=0&page=%s&t=%s'
response = s.get(data_url%(str(p),str(t)))
jsonobj = json.loads(response.text)
totalPage=jsonobj['totalPage']
list=jsonobj['list']
for e in jsonobj['list']:
    code=e[3]
    money=e[5]
    soup=BeautifulSoup(e[0],"html.parser")
    data_id=soup.span.attrs["data-id"]
    print(format_time(), p,data_id,code,money)
# print(jsonobj['list'])
# print(len(jsonobj['list']))
if totalPage >1:
    for i in range(2,totalPage+1):
        p=i
        response = s.get(data_url % (str(p), str(t)))
        jsonobj = json.loads(response.text)
        for e in jsonobj['list']:
            code = e[3]
            money = e[5]
            soup = BeautifulSoup(e[0], "html.parser")
            data_id = soup.span.attrs["data-id"]
            print(format_time(), p,data_id,code,money)
# http://ag1.kk688688.com/frommesg?__=frommesg&gameIndex=3&page=3&t=C587A1A9EB7479C84CB4F8AA8B32E290
# http://ag1.kk688688.com/frommesg?__=frommesg&gameIndex=3&settlement=0&beforeDate=2019-10-28&timesNum=20191028004&category_id=0&t=C587A1A9EB7479C84CB4F8AA8B32E290

from pygame import mixer # Load the required library
import time
mixer.init()
mixer.music.load('D:\\workspace\\pyProjects\\xmj-datawhale\\crawler\\wei\\tip.mp3')
mixer.music.play()
time.sleep(5)