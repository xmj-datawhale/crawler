# coding:utf-8
from urllib.request import Request
from urllib.request import urlopen
import urllib
import random
import requests
import traceback
import re
from selenium import webdriver




class Downloader(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

    def download(self, url):
        print('正在下载页面：{}'.format(url))
        try:
            resp = requests.get(url, headers=self.headers)

            if resp.status_code == 200:
                return resp.text
            else:
                raise ConnectionError
        except Exception:
            print('下载页面出错：{}'.format(url))
            traceback.print_exc()

    def get_ip_list(self, resp):
        try:
            # 匹配整体数据的正则
            root_pattren = 'alt="Cn" /></td>([\d\D]*?)</tr>'
            root = re.findall(root_pattren, resp)
            list_ip = []
            # 再次匹配数据的正则
            for i in range(len(root)):
                key = re.findall('<td>([\d\D]*?)</td>', root[i])
                list_ip.append(key[3].lower() + '://' + key[0] + ':' + key[1])
            return list_ip
        except Exception:
            print('解析IP地址出错')
            traceback.print_exc()

    def getHtml(url, proxies):
        proxy = random.choice(proxies)  # 随机取一个ip出来使用
        proxy_support = urllib.request.ProxyHandler({"http": proxy})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        html = urlopen(url)
        return html

# def main():
#     url = 'https://www.xicidaili.com/'
#     resp = Downloader().download(url)
#     info = Downloader().get_ip_list(resp)
#     for i in info:
#         print(i)
def main():
    url = 'https://www.xicidaili.com/'
    resp = Downloader().download(url)
    proxies = Downloader().get_ip_list(resp)
    # for i in info:
    #     print(i)
    info = Downloader().get_ip_list(resp)
    chromeOptions = webdriver.ChromeOptions()
    # 设置代理
    chromeOptions.add_argument("--proxy-server=http://60.13.42.60:9999")
    browser = webdriver.Chrome("D:\\360安全浏览器下载\\chromedriver_win32\\chromedriver.exe",chrome_options =chromeOptions)
    url = "https://mail.163.com/"
    url = "https://cn.mebtx4.com/sports/msports"
    browser.get(url)
    browser.maximize_window()
    browser.switch_to.frame(0)
    elem = browser.find_element_by_xpath('//*[@id="cnr-odds"]/div/div/div[3]/div/table/thead/tr[1]/th[1]')

    # req = requests.get('https://www.baidu.com', timeout=60, proxies={"http": "60.13.42.60:9999"})
    # print(req.content)
    # for i in info:
    #     try:
    #         print(i)
    #         iphead=i.split(":")[0]
    #         ip=i.split("//")[1]
    #         req = requests.get('https://www.baidu.com', timeout=60, proxies={iphead: ip})
    #         print(req.content)
    #     except:
    #         print("EX")
        # print(i)
    # for ip in proxies:
    #     try:
    #         # html = Downloader().getHtml(url, proxies)
    #         req = requests.get('https://www.baidu.com', timeout=60, proxies={ip})
    #         print(req.info())
    #         # print(i)
    #     except:
    #         print("故障")
    # for i in range(10000):
    #     try:
    #         # html = Downloader().getHtml(url, proxies)
    #         req = requests.get('https://www.baidu.com', timeout=60, proxies={'http': '59.173.73.112:3128'})
    #         print(html.info())
    #         print(i)
    #     except:
    #         print("故障")


if __name__ == '__main__':
    main()

