## 导入相关的库
import urllib
import requests
from bs4 import BeautifulSoup
def parse_content(content):
    soup = BeautifulSoup(content,'lxml')
    for i in soup.find_all("tbody"):
        try:
            name = i.find('div', class_="auth").get_text(strip=True)
            content = i.find('td', class_="postbody").get_text(strip=True)
            print(name + ":" + content)
        except:
            pass

def main():
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    request = urllib.request.Request(url=url,headers=headers)
    content = urllib.request.urlopen(request).read().decode()
    parse_content(content)

if __name__ == '__main__':
    main()