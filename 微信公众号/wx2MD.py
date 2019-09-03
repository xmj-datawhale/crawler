import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
def data2MD(_path):
    md_path = r'%s%s' % (_path, 'markdonw')
    csv_path = r'%s%s' % (_path, 'article.list.csv')
    if not os.path.exists(md_path):
        os.makedirs(md_path)
    summary_out=r'%s%s/summary.md'%(_path,'markdonw')
    df = pd.read_csv(open(csv_path,encoding='utf-8'), lineterminator='\n', header=0)
    for i in range(1,len(df['content_html'])):
        title=df.get('title').iloc[i]
        title=str(title).replace('/','-').replace(' ','')
        article_file='第%s篇-%s.md'%(str(i),str(title))
        with open(summary_out,mode='a',encoding='utf-8') as sf:
            sf.write('## [第%s篇  %s](%s) \n'%(str(i+1),str(title),str(article_file)))
        if type(df.get('content_html').iloc[i])!=str:
            continue
        context=str(df.get('content_html').iloc[i])[50:-6]
        with open('%s/%s'%(md_path,article_file), mode='a', encoding='utf-8') as f:
            f.write('## %s \n' % (str(article_file)[:-3]))
            f.write(context+'\n')

        if i%100==0:
            print("正在写入%s篇文章"%(str(i+1)))


if __name__ == '__main__':
    data2MD('./caoz的梦呓/')
    # pd.DataFrame(['asdf','vvvv']).to_csv('aa.csv')
    # pd.DataFrame(pd.read_csv('./caoz的梦呓//aa.csv', encoding='gbk',lineterminator='\n', header=0))
