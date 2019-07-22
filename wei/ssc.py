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
import numpy as np
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
my_account='yy66999'
webdriver.ChromeOptions.binary_location='./App/chrome.exe'
driver_proxy = webdriver.Chrome('chromedriver1.exe')

wait=WebDriverWait(driver_proxy,10)#等待
def proxy_login():
    """代理登录"""
    driver_proxy.get(url)
    # driver_proxy.maximize_window()
    wait=WebDriverWait(driver_proxy,10)#等待
    wait.until(EC.presence_of_element_located((By.ID,'passcode')))
    driver_proxy.find_element_by_xpath('//*[@id="passcode"]').send_keys(proxy_input_no)
    driver_proxy.find_element_by_xpath('//*[@id="submitbtn"]').click()
    """选择代理线路"""
    proxy_road=random.randint(1,8)
    print(format_time(),"选择代理线路%s" % str(proxy_road))
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[2]/a[{}]'.format(proxy_road))))
    href=driver_proxy.find_element(By.XPATH,'/html/body/div/div[2]/a[{}]'.format(proxy_road)).get_attribute('href')
    driver_proxy.get(href)
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Account"]')))
    print(format_time(),"代理帐号",account,"pwd:",pwd)
    driver_proxy.find_element(By.XPATH,'//*[@id="Account"]').send_keys(account)
    driver_proxy.find_element(By.XPATH,'//*[@id="Password"]').send_keys(pwd)
    driver_proxy.find_element(By.XPATH,'//*[@id="btn-submit"]').click()
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="agree"]')))
    driver_proxy.find_element(By.XPATH,'//*[@id="agree"]').click()
try:
    proxy_login()
except:
    print(format_time(),"代理登录失败")
    sleep(3)
    proxy_login()
else:
    print(format_time(),"代理登录成功")
# wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="agree"]')))
# sleep(4)
# while True:
#     if driver_proxy.find_element_by_xpath('//*[@id="agree"]').get_attribute('value')=='同意':
#         driver_proxy.find_element(By.XPATH, '//*[@id="agree"]').click()
#         break
#     sleep(1)
"""代理登录end"""

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
while True:
    try:
        list = []
        """10分钟清理一起下注清单"""
        if time.time()-login_time >10*60:
            list,downed_order_no_list,login_time=[],[],time.time()
            a_banlance = driver_account.find_elements(By.XPATH, '//*[@id="Cash"]')[0].text
            print(format_time(),"5分钟清理一起下注清单", "余额", a_banlance)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wagers_manager_link"]/span')))
        driver_proxy.find_element(By.XPATH, '//*[@id="wagers_manager_link"]/span').click()
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="SeleAccount"]')))
        # driver_proxy.find_element(By.XPATH, '//*[@id="SeleAccount"]').send_keys(search_account)
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gbGrid"]/a[2]')))
        # while True:
        #     if len(driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/a[2]')) >0:
        #         break
        #     else:
        #         sleep(5)
        # driver_proxy.find_element(By.XPATH, '//*[@id="gbGrid"]/a[2]').click()
        """获取分页数据"""
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id = "gbGrid"]/div/a[4]')))
        total_str = driver_proxy.find_elements(By.XPATH, '//*[ @ id = "gbGrid"]/div /a[4]')[0].text
        num = re.findall('\d+', total_str)[0]
        wait.until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "showGameNum"]')))
        term_no=driver_proxy.find_elements(By.XPATH, '// *[ @ id = "showGameNum"]')[0].text
        print(format_time(),term_no,100*"*")
        down_index=0
        for _ in range(int(num)):
            trs_len = len(driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr'))
            print(format_time(), "正在获取第%s页数据,一共%d 组" % (_,trs_len))
            # for j in  range(3):
            #     list.append({"o_no":"001", "o_t":"","o_code":"6785", "o_account":"", "o_term_no":"", "o_momey":"1"})

            for i in range(trs_len):
                if i == 0:
                    continue
                o_account = driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr[{}]/td[3]'.format(i + 1))[0].text
                # print(o_account == search_account)
                if o_account == search_account \
                        or 1==1:
                    o_no = driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr[{}]/td[1]'.format(i + 1))[0].text
                    o_t = driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr[{}]/td[2]'.format(i + 1))[ 0].text
                    o_term_no = driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr[{}]/td[4]'.format(i + 1))[0].text
                    o_code = driver_proxy.find_elements(By.XPATH, '// *[ @ id = "gbGrid"] / table / tbody / tr[{}] / td[5] / font[2]'.format(i + 1))[0].text
                    o_code=str.replace(o_code,'(','')
                    o_code = str.replace(o_code, ')', '')
                    o_momey = driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/table/tbody/tr[{}]/td[7]'.format(i + 1))[0].text
                    # print(format_time(),o_no, o_t, o_account, o_term_no, o_momey,o_code)
                    # list.append({"o_no":o_no, "o_t":o_t,"o_code":o_code, "o_account":o_account, "o_term_no":o_term_no, "o_momey":o_momey})
                    list.append({"o_no":str(o_no), "o_t":str(o_t),"o_code":str(o_code), "o_account":str(o_account), "o_term_no":str(o_term_no), "o_momey":str(o_momey)})
                    if o_code in downed_order_no_list:
                        continue
                    down_gold = 1
                    # driver_account.find_element(By.XPATH,'//*[@id="NumType"]').click()
                    driver_account.find_element(By.XPATH, '//*[@id="number"]').send_keys(o_code)
                    driver_account.find_element(By.XPATH, '//*[@id="gold"]').send_keys(down_gold)
                    # sleep(1)
                    driver_account.find_element(By.XPATH, '//*[@id="kuaida"]/div[2]/div/table[2]/tbody/tr/td[3]/input[1]').click()
                    downed_order_no_list.append(o_code)
                    print(format_time(), "下注：", o_code, down_gold)
                    down_index+=1
                    sleep(0.5)
            """下一页"""
            wait.until(EC.presence_of_element_located((By.XPATH, '// *[@id="gbGrid"]/div/a[5]')))
            driver_proxy.find_element(By.XPATH, '// *[@id="gbGrid"]/div/a[5]').click()
            sleep(3)

        # np.savetxt(format_filename()+".csv",list)
        print(format_time(),"下注总数：",down_index)
        # if list is not  None and len(list)>0:
        #     """下注"""
        #     if len(driver_account.find_elements(By.XPATH, '//*[@id="main"]/div/div/div/table/tbody/tr/td/div')) > 0 \
        #             and driver_account.find_elements(By.XPATH, '//*[@id="main"]/div/div/div/table/tbody/tr/td/div')[0].text == '已封盘':
        #         print(format_time(),"已封盘,未能下注:",list)
        #         list.clear()
        #         sleep(10)
        #         continue
        #     for down in list:
        #         down_order_no=down['o_no']
        #         down_code = down['o_code']
        #         down_gold = down['o_momey']
        #         # down_gold=1#默认下注金额 1
        #         if down_order_no in downed_order_no_list:
        #             continue
        #         down_gold = 1
        #         # driver_account.find_element(By.XPATH,'//*[@id="NumType"]').click()
        #         driver_account.find_element(By.XPATH, '//*[@id="number"]').send_keys(down_code)
        #         driver_account.find_element(By.XPATH, '//*[@id="gold"]').send_keys(down_gold)
        #         # sleep(1)
        #         # driver_account.find_element(By.XPATH, '//*[@id="kuaida"]/div[2]/div/table[2]/tbody/tr/td[3]/input[1]').click()
        #         downed_order_no_list.append(down_order_no)
        #         print(format_time(),"下注：",down_code,down_gold)
        #         sleep(0.5)
        #     list=[]
        #     wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gbGrid"]/a[2]')))
        #     while True:
        #         if len(driver_proxy.find_elements(By.XPATH, '//*[@id="gbGrid"]/a[2]')) >0:
        #             break
        #         else:
        #             sleep(5)
        #     driver_proxy.find_element(By.XPATH, '//*[@id="gbGrid"]/a[2]').click()

        sleep(5)
    except Exception:
        # print("会员异常刷新")
        driver_account.refresh()
        sleep(5)

driver_proxy.close()