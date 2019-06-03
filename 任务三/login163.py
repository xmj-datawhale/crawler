import time
from selenium import webdriver

# from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome("D:\\360安全浏览器下载\\chromedriver_win32\\chromedriver.exe")
url = "https://mail.163.com/"
url = "https://cn.mebtx4.com/sports/msports"
browser.get(url)
browser.maximize_window()
browser.switch_to.frame(0)

# self.assertIn("Python", driver.title)
elem = browser.find_element_by_xpath('//*[@id="cnr-odds"]/div/div/div[3]/div/table/thead/tr[1]/th[1]')

