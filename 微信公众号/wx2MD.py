import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
def data2MD(_path):
    md_path = r'%s%s' % (_path, 'markdonw')
    csv_path = r'%s%s' % (_path, 'article.list.csv')
    if not os.path.exists(md_path):
        os.makedirs(md_path)
    summary_out=r'%s%s/summary.md'%(_path,'markdonw')
    df = pd.read_csv(open(csv_path,encoding='utf-8'), lineterminator='\n', header=0)
    for i in range(1,len(df['content_html'])):
        title=df.get('title').iloc[i]
        title=validateTitle(title)
        # title=str(title).replace('/','-').replace(' ','')
        article_file='第%s篇-%s.md'%(str(i),str(title).replace('/','-').replace(' ',''))
        with open(summary_out,mode='a',encoding='utf-8') as sf:
            sf.write('## [第%s篇  %s](%s) \n'%(str(i+1),str(title),str(article_file)))
        if type(df.get('content_html').iloc[i])!=str:
            continue
        context=str(df.get('content_html').iloc[i])[50:-6]
        with open('%s/%s'%(md_path,article_file), mode='w', encoding='utf-8') as f:
            f.write('## %s \n%s\n' % (str(article_file)[:-3],context))

        if i%100==0:
            print("%s正在写入%s篇文章"%(str(_path),str(i+1)))
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
wx_list=[
         {'id':'MjM5ODIyMTE0MA==','name':'小道消息'},
         {'id':'MzI2OTM2NzA2OA==','name':'亦无所知'},
         {'id':'MzI2MzE2NDczMw==','name':'半佛仙人'},
         {'id':'MzA4NTQwNDcyMA==','name':'stormzhang'},
         # {'id':'MzIxODUxMDM5MQ==','name':'多元思维Hack'},
         # {'id':'MzI5MTE2NDI2OQ==','name':'仙人jump'},
         ]

if __name__ == '__main__':
    for e in wx_list:
        wx_id = e['id']
        wx_name = e['name']
        wx_offset = 0
        data2MD('./data/{0}/'.format(wx_name))
    # pd.DataFrame(['asdf','vvvv']).to_csv('aa.csv')
    # pd.DataFrame(pd.read_csv('./caoz的梦呓//aa.csv', encoding='gbk',lineterminator='\n', header=0))
