# 3.1 Task5  安装selenium并学习
## 安装selenium并学习。
* 使用selenium模拟登陆163邮箱。
163邮箱直通点：https://mail.163.com/ 。
参考资料：https://blog.csdn.net/weixin_42937385/article/details/88150379
 ### 基本使用
 ```angular2html
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
 
browser=webdriver.Chrome()#声明一个浏览器对象
try:
    browser.get("https://www.baidu.com")#传入URL
    input=browser.find_element_by_id('kw')#找到网页中id为kw的元素，即百度中的搜索框
    input.send_keys('Python')#输入搜索的内容
    input.send_keys(Keys.ENTER)#回车
    wait=WebDriverWait(browser,10)#等待
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()
```
### 模拟登录 163
```angular2html
import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
 
browser=webdriver.Chrome()
url="https://mail.163.com/"
browser.get(url)
browser.maximize_window()
browser.switch_to.frame(0)
email=browser.find_element_by_name('email')
email.send_keys('*******@163.com')
password=browser.find_element_by_name('password')
password.send_keys('*********')
login_em=browser.find_element_by_id('dologin')
login_em.click()

```
# 3.2 Task6 学习IP相关知识
## 学习什么是IP，为什么会出现IP被封，如何应对IP被封的问题。
* 抓取西刺代理，并构建自己的代理池。
 西刺直通点：https://www.xicidaili.com/ 。
 
### 定义
互联网协议地址（Internet Protocol Address，又译为网际协议地址），缩写为IP地址（IP Address），是分配给用户上网使用的网际协议（IP）的设备的数字标签。常见的IP地址分为IPv4与IPv6两大类，但是也有其他不常用的小分类。

基本原理
网络互连设备，如以太网、分组交换网等，它们相互之间不能互通，不能互通的主要原因是因为它们所传送数据的基本单元（技术上称之为“帧”）的格式不同。IP协议实际上是一套由软件、程序组成的协议软件，它把各种不同“帧”统一转换成“网协数据包”格式，这种转换是因特网的一个最重要的特点，使所有各种计算机都能在因特网上实现互通，即具有“开放性”的特点。

IP地址
（1）IP地址由32位二进制数组成，为便于使用，常以XXX.XXX.XXX.XXX形式表现，每组XXX代表小于或等于255的10进制数。地址可分为A、B、C、D、E五大类，其中E类属于特殊保留地址。
（2）用来在网络中标记一台电脑的一串数字，每个IP地址包括两部分，网络地址和主机地址。网络地址的最高位必须是0。
（3）子网掩码的作用是将IP地址划分成网络地址和主机地址两部分。子网掩码不能单独存在，必须与IP地址一起使用。
（4）主机号全为0，表示网络号；主机号全为1，表示网络广播。

为什么会出现IP被封
### 定义
IP封锁是指防火墙维护一张IP黑名单，一旦发现发往黑名单中地址的请求数据包，就直接将其丢弃，这将导致源主机得不到目标主机的及时响应而引发超时，从而达到屏蔽对目标主机的访问的目的。
IP被封的原因
（1）服务器在国内被封，无法正常访问。
（2）网站采取了一些反爬的措施，比如，服务器会检测某个IP在单位时间内的请求次数，如果超过某个阀值，那么服务器会直接拒绝服务，返回一些错误信息。
（3）服务商更换服务器（不常见）。

### 如何应对IP被封的问题

1.伪造User-Agent
在请求头中把User-Agent设置成浏览器中的User-Agent，来伪造浏览器访问。
还可以先收集多种浏览器的User-Agent，每次发起请求时随机从中选一个使用，可以进一步提高安全性。
2.在每次重复爬取之间设置一个随机时间间隔
3.伪造cookies
若从浏览器中可以正常访问一个页面，则可以将浏览器中的cookies复制过来使用
4. 使用代理
可以换着用多个代理IP来进行访问，防止同一个IP发起过多请求而被封IP

 
 
 ```angular2html
import requests
import traceback
import re

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

def main():
    url = 'https://www.xicidaili.com/'
    resp = Downloader().download(url)
    info = Downloader().get_ip_list(resp)
    for i in info:
        print(i)


if __name__ == '__main__':
    main()
```
 
参考资料：https://blog.csdn.net/weixin_43720396/article/details/88218204
浏览器下载驱动地址：
https://sites.google.com/a/chromium.org/chromedriver/downloads