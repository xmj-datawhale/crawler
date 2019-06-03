import urllib.request
from lxml import etree

def parse_content(content):
    tree = etree.HTML(content)
    name_list = tree.xpath('//*[@class="postbox"]//tbody//*[@class="auth"]/a/text()')
    content_list = tree.xpath('//*[@class="postbox"]//tbody//*[@class="postbody"]')
    for i,j in zip(name_list,content_list):
        j = j.text.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        print('{}:{}'.format(i,j))

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