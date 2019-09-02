import re
import requests
import json
import os
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import quote

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>{title}</h1>
<p>{text}</p>
</body>
</html>
"""
htmls = []
num = 0
def get_data(url):

    global htmls, num
        
    headers = {
        'Authorization': 'DD282FEB-EDD7-A50E-6C94-344947B6E723',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    headers = {
        'accept': "application/json, text/plain, */*",
        'origin': "https://wx.zsxq.com",
        'x-version': "1.10.14",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        'x-request-id': "49b20ff1-e43b-27eb-4483-c2ef7e69c4ae",
        'Authorization':"49b20ff1-e43b-27eb-4483-c2ef7e69c4ae",
        'x-signature': "fd4d05f5f11d006a4ef2e5df89bcef92f2f3bdbe",
        'referer': "https://wx.zsxq.com/dweb/",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
        # 'cookie': "zsxq_access_token=zsxq.py;UM_distinctid=16ca80bddd0383-0ecd3b4229e928-37c143e-1fa400-16ca80bddd1486;avatar_url=https%3A//images.zsxq.com/Fvv1wVWMXu_isO64oXhGYlmHoErr%3Fe%3D1906272000%26token%3DkIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD%3ATQapZjuttp1LcCGTVFlWFx6UJ_k%3D&name=%u661F%u671F%u516B&upload_channel=qiniu&user_id=548284811158524&ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3D42680B01-00F7-545C-DAE8-0E209D2D6C41&zsxq_access_token=42680B01-00F7-545C-DAE8-0E209D2D6C41",
        # 'cookie': "UM_distinctid=16c6ed8296f4ee-087749adad3d-36664c08-1fa400-16c6ed8297122; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c92fd13ba45b-0a0bae5b564ac-36664c08-2073600-16c92fd13bc382%22%2C%22%24device_id%22%3A%2216c92fd13ba45b-0a0bae5b564ac-36664c08-2073600-16c92fd13bc382%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; zsxq_access_token=9C5814CB-E434-B07B-906B-CC569F795D75"
        'cookie': "_uab_collina=156636875770574735449994; \
        avatar_url=https%3A//images.zsxq.com/Fvv1wVWMXu_isO64oXhGYlmHoErr%3Fe%3D1906272000%26token%3DkIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD%3ATQapZjuttp1LcCGTVFlWFx6UJ_k%3D;\
        name=%u661F%u671F%u516B;\
        upload_channel=qiniu;\
        UM_distinctid=16cb2da72810-0e3b3efa303afb8-4c312272-1fa400-16cb2da728281;\
        user_id=548284811158524;\
        ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3DEBD821B5-2B4D-DFC9-BD82-269062F46511;\
        zsxq_access_token=EBD821B5-2B4D-DFC9-BD82-269062F46511;"

    }
    
    rsp = requests.get(url, headers=headers)
    with open('test.json', 'w', encoding='utf-8') as f:        # 将返回数据写入 test.json 方便查看
        f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))
    
    with open('test.json', encoding='utf-8') as f:
        for topic in json.loads(f.read()).get('resp_data').get('topics'):
            content = topic.get('question', topic.get('talk', topic.get('task', topic.get('solution'))))
            # print(content)
            text = content.get('text', '')
            text = re.sub(r'<[^>]*>', '', text).strip()
            text = text.replace('\n', '<br>')
            title = str(num) + text[:9]
            num += 1

            if content.get('images'):
                soup = BeautifulSoup(html_template, 'html.parser')
                for img in content.get('images'):
                    url = img.get('large').get('url')
                    img_tag = soup.new_tag('img', src=url)
                    soup.body.append(img_tag)
                    html_img = str(soup)
                    html = html_img.format(title=title, text=text)
            else:
                html = html_template.format(title=title, text=text)

            if topic.get('question'):
                answer = topic.get('answer').get('text', "")
                soup = BeautifulSoup(html, 'html.parser')
                answer_tag = soup.new_tag('p')
                answer_tag.string = answer
                soup.body.append(answer_tag)
                html_answer = str(soup)
                html = html_answer.format(title=title, text=text)

            htmls.append(html)

    next_page = rsp.json().get('resp_data').get('topics')
    if next_page:
        create_time = next_page[-1].get('create_time')
        if create_time[20:23] == "000":
            end_time = create_time[:20]+"999"+create_time[23:]
        else :
            res = int(create_time[20:23])-1
            end_time = create_time[:20]+str(res).zfill(3)+create_time[23:] # zfill 函数补足结果前面的零，始终为3位数
        end_time = quote(end_time)
        if len(end_time) == 33:
            end_time = end_time[:24] + '0' + end_time[24:]
        next_url = start_url + '&end_time=' + end_time
        print(next_url)
        get_data(next_url)

    return htmls

def make_pdf(htmls):
    html_files = []
    for index, html in enumerate(htmls):
        file = str(index) + ".html"
        html_files.append(file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)

    options = {
        "user-style-sheet": "test.css",
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [
            ("cookie-name1", "cookie-value1"), ("cookie-name2", "cookie-value2")
        ],
        "outline-depth": 10,
    }
    try:
        path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # wkhtmltopdf安装位置
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        pdfkit.from_file(html_files, "电子书1.pdf", options=options,configuration=config)
    except Exception as e:
        pass

    for file in html_files:
        os.remove(file)

    print("已制作电子书在当前目录！")

if __name__ == '__main__':
    # 144818158482
    start_url = 'https://api.zsxq.com/v1.10/groups/144818158482/topics?scope=digests&count=20'
    make_pdf(get_data(start_url))
