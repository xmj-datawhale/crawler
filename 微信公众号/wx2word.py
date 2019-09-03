import requests
from bs4 import BeautifulSoup
import pandas as pd

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>{title}</h1>
<br>{author} - {cretime}<br>
<br>{index_tag}<br>
<p>{text}</p>
</body>
</html>
"""

def data2MD(_path,output):

    df = pd.read_csv(open(_path,encoding='utf-8'), lineterminator='\n', header=0)
    for i in range(1,len(df['content_html'])):
        html_template.
        title=df.get('title').iloc[i]
        context=str(df.get('content_html').iloc[i])[50:-6]
        str_content='## %s\n %s\n'%(title,context)
        with open(output,'a',encoding='utf-8') as f:
            f.write(str_content)

if __name__ == '__main__':
    data2MD('./caoz的梦呓/article.list.csv','./caoz的梦呓/article.list.md')
    # pd.DataFrame(['asdf','vvvv']).to_csv('aa.csv')
    # pd.DataFrame(pd.read_csv('./caoz的梦呓//aa.csv', encoding='gbk',lineterminator='\n', header=0))
