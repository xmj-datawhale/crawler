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
downloadedNum=25
def login_zsxq(url, groupName):
    try:
        # chromeOptions = webdriver.ChromeOptions()
        # # prefs = {"download.default_directory": "D:\\downlowd\\%s\\"%(groupName)}
        # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': "D:\\downloads\\%s\\"%(groupName)}
        # chromeOptions.add_experimental_option("prefs", prefs)
        webdriver.ChromeOptions.binary_location = './App/chrome.exe'
        driver_zsxq = webdriver.Chrome('chromedriver1.exe')
        """代理登录"""
        driver_zsxq.get(url)
        driver_zsxq.maximize_window()
        wait = WebDriverWait(driver_zsxq, 30)  # 等待
        wait.until(EC.presence_of_element_located((By.XPATH,
                                                   '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/div/xmq-editor/div/div/div[1]/div[2]/label[4]/span[2]')))
        while True:
            e1 = driver_zsxq.find_elements_by_xpath(
                '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/div/xmq-editor/div/div/div[1]/div[2]/label[4]/span[2]')
            if (e1 != None and len(e1) > 0 and str.strip(e1[0].text) == '文章'):
                break
            else:
                time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="leftgroup"]/div[1]/div/ul/li[*]')))
        groupList = driver_zsxq.find_elements_by_xpath( '//*[@id="leftgroup"]/div[1]/div/ul/li[*]')
        if (groupList != None and len(groupList) > 0):
            for e in groupList:
                if e.text == str.strip(groupName):
                    e.click()

        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="menuright"]/div[1]/xmq-introduction/div/div[2]/div')))
        while True:
            e2 = driver_zsxq.find_elements_by_xpath('//*[@id="menuright"]/div[1]/xmq-introduction/div/div[2]/div')
            if (e2 != None and len(e2) > 0 and str.strip(e2[0].text) == str.strip(groupName)):
                break
            else:
                time.sleep(1)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'file-a')))
        #         鼠标停留让元素出现
        ActionChains(driver_zsxq).move_to_element(driver_zsxq.find_element_by_class_name("file-a")).perform()
        sleep(1)
        while True:
            e3 = driver_zsxq.find_element_by_class_name("file-a")
            if (e3 != None and e3.text=='查看全部'):
                break
        driver_zsxq.find_element_by_class_name("file-a").click()

        # ActionChains(driver_zsxq).move_to_element(driver_zsxq.find_element_by_class_name("file-a")[0]).perform()
        # document.getElementsByClassName('file-a')[0].scrollBy(1268, 860)


        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul')))
        while True:
            e4 = driver_zsxq.find_elements_by_xpath('/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[*]/div/p[1]')
            if (e4 != None and len(e4) > 0):
                break;
        downFiles=0
        fileTotal=0
        _fileTotal = 0
        driver_zsxq.execute_script("window.scrollBy(1268,%d)" % (( 1) * 1000))
        for j in range(10):
            _fileTotal=len(driver_zsxq.find_elements_by_xpath(
                '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[*]/div/p[1]'))
            if fileTotal==_fileTotal:
                break
            # for i in range(fileTotal,_fileTotal):
            #     wait.until(EC.presence_of_element_located((By.XPATH,
            #                                                '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[%s]/div/p[1]' % (
            #                                                            i + 1))))
            #     e5 = driver_zsxq.find_elements_by_xpath(
            #         '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[%s]/div/p[1]' % (
            #                 i + 1))
            #     if (e5 != None and len(e5) > 0):
            #         ActionChains(driver_zsxq).move_to_element(e5[0]).perform()
            #         time.sleep(2)
            #         e5[0].click()
            #         time.sleep(2)
            #         driver_zsxq.find_element_by_xpath(
            #             '/html/body/xmq-web/xmq-index/div/div[1]/div[2]/xmq-filepreview/div/div[2]/a').click()
            #         time.sleep(2)
            #         ActionChains(driver_zsxq).move_by_offset(-10, -10).click().perform()
            fileTotal=_fileTotal
            driver_zsxq.execute_script("window.scrollBy(1268,%d)" % ((j + 1) * 1000))
            sleep(5)
            print("文件个数%d"%(fileTotal))
        for i in range(fileTotal, _fileTotal):
            wait.until(EC.presence_of_element_located((By.XPATH,
                                                       '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[%s]/div/p[1]' % (
                                                               i + 25))))
            e5 = driver_zsxq.find_elements_by_xpath(
                '/html/body/xmq-web/xmq-index/div/div[1]/div[1]/xmq-filelist/div/div[1]/div[3]/ul/li[%s]/div/p[1]' % (
                        i + 25))
            if (e5 != None and len(e5) > 0):
                ActionChains(driver_zsxq).move_to_element(e5[0]).perform()
                time.sleep(2)
                e5[0].click()
                time.sleep(2)
                driver_zsxq.find_element_by_xpath(
                    '/html/body/xmq-web/xmq-index/div/div[1]/div[2]/xmq-filepreview/div/div[2]/a').click()
                time.sleep(2)
                ActionChains(driver_zsxq).move_by_offset(-10, -10).click().perform()

    except Exception as e:
        print(e)
        # 报错后就强制停止加载
        # 这里是js控制
        # login_zsxq("https://wx.zsxq.com/dweb/#/login", "壹鸽技术工程")
        # driver_zsxq.execute_script('window.stop()')
        # print(driver_zsxq.page_source)



login_zsxq("https://wx.zsxq.com/dweb/#/login", "壹鸽技术工程")
# login_zsxq("https://wx.zsxq.com/dweb/#/login", "暴力引流术与道")