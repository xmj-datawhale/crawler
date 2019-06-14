from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
'''爬取极客时间栏目：｛课程名、课程数、学习课程的人数｝'''
# driver = webdriver.Chrome('E:\\workspace\\pyProjects\\apps\\chaobin\\selenium\\chromedriver.exe')
webdriver.ChromeOptions.binary_location='F:\\download\\GoogleChrome增强版\\Chrome_X64_75.0.3770.90\\App\\chrome.exe'
driver = webdriver.Chrome('E:\\workspace\\pyProjects\\apps\\chaobin\\selenium\\chromedriver1.exe')
url='http://news.sina.com.cn/o/2004-07-06/10433003819s.shtml'
url='https://time.geekbang.org/'
driver.get(url)
driver.maximize_window()

wait=WebDriverWait(driver,10)#等待
wait.until(EC.presence_of_element_located((By.CLASS_NAME,'_3G50nw0p_0')))
# e=driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/h2')

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # WebDriverWait(driver, 50)
    sleep(0.5)
    if len(driver.find_elements(By.CLASS_NAME,'vUoikev7_0')) > 0 :
        break

while True:
    driver.find_element(By.CLASS_NAME,'vUoikev7_0').click()
    sleep(0.5)
    if len(driver.find_elements(By.CLASS_NAME,'OjL5wNoM_0')) > 0  and driver.find_element(By.CLASS_NAME,'OjL5wNoM_0').text!='加载更多':
        break

list=driver.find_elements_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[*]/div[2]/div[1]/div[1]')
for e in list:
    title=str.split(e.text,'\n')[0]
    lesson_no=str.split(e.text,'\n')[1].split('|')[0].strip().split('讲')[0]
    learning_no=str.split(e.text,'\n')[1].split('|')[1].strip().split('人')[0]
    # print('{},{},{}'.format(title,lesson_no,learning_no))
    print('%s,%s,%s'%(title,lesson_no,learning_no))
driver.close()