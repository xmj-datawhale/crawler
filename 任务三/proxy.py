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
