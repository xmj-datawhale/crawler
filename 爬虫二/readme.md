# 学习beautifulsoup
- 学习beautifulsoup，并使用beautifulsoup提取内容。
- 使用beautifulsoup提取丁香园论坛的回复内容。
- 丁香园直通点：http://www.dxy.cn/bbs/thread/626626#626626 。
- 参考资料：https://blog.csdn.net/wwq114/article/details/88085875
* Beautiful Soup 是用Python写的一个HTML/XML的解析器，它可以很好的处理不规范标记并生成剖析树(parse
tree)。 它提供简单又常用的导航（navigating），搜索以及修改剖析树的操作。它可以大大节省你的编程时间。
对于Ruby，使用Rubyful Soup。
``````angular2html
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
``````
```angular2html
楼医生:我遇到一个“怪”病人，向大家请教。她，42岁。反复惊吓后晕厥30余年。每次受响声惊吓后发生跌倒，短暂意识丧失。无逆行性遗忘，无抽搐，无口吐白沫，无大小便失禁。多次跌倒致外伤。婴儿时有惊厥史。入院查体无殊。ECG、24小时动态心电图无殊；头颅MRI示小软化灶；脑电图无殊。入院后有数次类似发作。请问该患者该做何诊断，还需做什么检查，治疗方案怎样？
lion000:从发作的症状上比较符合血管迷走神经性晕厥，直立倾斜试验能协助诊断。在行直立倾斜实验前应该做常规的体格检查、ECG、UCG、holter和X-ray胸片除外器质性心脏病。贴一篇“口服氨酰心安和依那普利治疗血管迷走性晕厥的疗效观察”作者：林文华 任自文 丁燕生http://www.ccheart.com.cn/ccheart_site/Templates/jieru/200011/1-1.htm
xghrh:同意lion000版主的观点：如果此患者随着年龄的增长，其发作频率逐渐减少且更加支持，不知此患者有无这一特点。入院后的HOLTER及血压监测对此患者只能是一种安慰性的检查，因在这些检查过程中患者发病的机会不是太大，当然不排除正好发作的情况。对此患者应常规作直立倾斜试验，如果没有诱发出，再考虑有无可能是其他原因所致的意识障碍，如室性心动过速等，但这需要电生理尤其是心腔内电生理的检查，毕竟是有一种创伤性方法。因在外地，下面一篇文章可能对您有助，请您自己查找一下。心理应激事件诱发血管迷走性晕厥1例 ，杨峻青、吴沃栋、张瑞云，中国神经精神疾病杂志， 2002 Vol.28 No.2
keys:该例不排除精神因素导致的，因为每次均在受惊吓后出现。当然，在作出此诊断前，应完善相关检查，如头颅MIR(MRA),直立倾斜试验等。
```
# 2.2 Task4 学习xpath 
- 学习xpath，使用lxml+xpath提取内容。
- 使用xpath提取丁香园论坛的回复内容。
- 丁香园直通点：http://www.dxy.cn/bbs/thread/626626#626626 。
- 参考资料：https://blog.csdn.net/naonao77/article/details/88129994


``````angular2html
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
``````
```angular2html
C:\ProgramData\Anaconda3\python.exe D:/workspace-py/datawhale/datawhale/crawler/爬虫二/xpath_task.py
楼医生:我遇到一个“怪”病人，向大家请教。她，42岁。反复惊吓后晕厥30余年。每次受响声惊吓后发生跌倒，短暂意识丧失。无逆行性遗忘，无抽搐，无口吐白沫，无大小便失禁。多次跌倒致外伤。婴儿时有惊厥史。入院查体无殊。ECG、24小时动态心电图无殊；头颅MRI示小软化灶；脑电图无殊。入院后有数次类似发作。请问该患者该做何诊断，还需做什么检查，治疗方案怎样？
lion000:从发作的症状上比较符合血管迷走神经性晕厥，直立倾斜试验能协助诊断。在行直立倾斜实验前应该做常规的体格检查、ECG、UCG、holter和X-ray胸片除外器质性心脏病。
xghrh:同意lion000版主的观点：如果此患者随着年龄的增长，其发作频率逐渐减少且更加支持，不知此患者有无这一特点。
keys:该例不排除精神因素导致的，因为每次均在受惊吓后出现。当然，在作出此诊断前，应完善相关检查，如头颅MIR(MRA),直立倾斜试验等。
```