# 实战大项目
模拟登录丁香园，并抓取论坛页面所有的人员基本信息与回复帖子内容。
# ccookies 设置
```angular2html
cookies = {
            'cookie': '你的cookies'
        }
        url = 'http://www.dxy.cn/bbs/thread/626626#626626'
        req = requests.get(url, cookies=cookies)  #

```

```angular2html
import requests
from bs4 import BeautifulSoup
import selenium


class Taks7:
    def __init__(self):
        pass

    def get_info(self):
        data = {}
        data2 = {}
        cookies = {
            'cookie': 'your cookie'
        }
        url = 'http://www.dxy.cn/bbs/thread/626626#626626'
        req = requests.get(url, cookies=cookies)  #
        soup = BeautifulSoup(req.text, 'html.parser')
        title = soup.find('title')
        data['title'] = title.text
        author_say_tags = soup.find('meta', attrs={'property': "og:description"})
        author_say_tag = author_say_tags.attrs
        author_say = author_say_tag['content']
        details = soup.find_all('div', attrs={'class': 'info clearfix'})
        user_atten = soup.find_all('div', attrs={'class': 'user_atten'})
        auth_name = soup.find_all('div', attrs={'class': "auth"})
        data['author_say'] = author_say
        recoverys = soup.find_all('td', attrs={'class': "postbody"})
        for i in range(len(recoverys)):
            data['auth_name'] = auth_name[i].text
            data['user_atten'] = user_atten[i].text.strip().split()
            data['info_clearfix'] = details[i].text.replace('\n', '')
            data['recovery'] = recoverys[i].text.strip()

            print(data)


a = Taks7().get_info()


```
- 丁香园论坛：http://www.dxy.cn/bbs/thread/626626#626626 。

参考文章：
https://blog.csdn.net/dfy20020530/article/details/89282386