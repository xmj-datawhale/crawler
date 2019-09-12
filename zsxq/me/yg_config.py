from urllib.request import quote
NEW_LATE_DATE  = '2019-09-01 00:00:00' # 最晚时间
NEW_EARLY_DATE = '2017-03-17 00:00:00'# 最早时间
GROUP_ID = '455488242588'                                  # 知识星球中的小组ID
FILE_NAME               = '壹鸽技术工程'                    # 生成文件的名字
DOWLOAD_FILES           = True                                        # 是否下载文件 True | False 下载会导致程序变慢
DOWLOAD_PICS            = True                                        # 是否下载图片 True | False 下载会导致程序变慢
DOWLOAD_COMMENTS        = True                                    # 是否下载评论
ONLY_DIGESTS            = False                                       # True-只精华 | False-全部
FROM_DATE_TO_DATE       = True                                  # 按时间区间下载

DELETE_PICS_WHEN_DONE   = False                               # 运行完毕后是否删除下载的图片
DELETE_HTML_WHEN_DONE   = False                               # 运行完毕后是否删除生成的HTML
COUNTS_PER_TIME         = 30                                  # 每次请求加载几个主题 最大可设置为30
DEBUG                   = False                               # DEBUG开关
DEBUG_NUM               = 120                                 # DEBUG时 跑多少条数据后停止 需与COUNTS_PER_TIME结合考虑
DATA_DIR                =r'F:/知识星球/壹鸽技术工程/20190829-7'
DATA_ROOT               =r'F:/知识星球/壹鸽技术工程'
FILE_DOWNLOAD_DIR       = r'F:/知识星球/壹鸽技术工程/ALL_FILE'
FILE_DOWNLOAD_URL       = 'https://api.zsxq.com/v1.10/files/%s/download_url'
ALL_FILE_URL            = 'https://api.zsxq.com/v1.10/groups/%s/files?count=%s&end_time=%s' # [end_time-1]'https://api.zsxq.com/v1.10/groups/455488242588/files?count=20&end_time=2019-06-13T16%3A19%3A29.514%2B0800'
COLUMNS                 = ['NUM','html_url', '主题ID', '主题标签', '创建时间','作者', '阅读数', '点赞数', '评论数', '回复数', '是否精华','是否问答', '是否文件','主题内容']#主题字段
DOWNLOAD_FILE_COLUMNS   = ['文件名称', '主题ID', '文件ID', '创建时间','作者', '下载数', '文件大小', '本地文件名称']#主题下载字段

TOPIC_SAVE_FILE         ='topics.csv'
TOPIC_FILE_SAVE_FILE    ='topic_files.csv'

PATH_WK = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'#wkhtmltopdf 安装位置
DIGESTS_URL = 'https://api.zsxq.com/v1.10/groups/%s/topics?scope=digests&count=%s&end_time=%s'
# TOPIC_URL = 'https://api.zsxq.com/v1.10/groups/%s/topics?scope=digests&count=%s&end_time=%s'
TOPIC_URL = 'https://api.zsxq.com/v1.10/groups/%s/topics?count=%s&end_time=%s'
ALL_COMTENT_URL = 'https://api.zsxq.com/v1.10/topics/%s/comments?count=%s&sort=asc&begin_time=%s'



# DATA_DIR='%s-%s'%(str.replace(EARLY_DATE[:10],'-',''),str.replace(LATE_DATE[:10],'-',''))

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

UM_distinctid="16cb2da72810-0e3b3efa303afb8-4c312272-1fa400-16cb2da728281";
_uab_collina="156636875770574735449994";
name=quote("星期八");
upload_channel="qiniu";
user_id="15142221115542";
ws_address="wss://ws.zsxq.com/ws?version=v1.10&access_token=0CBBBCD4-1A68-0BD3-AD93-124745DB5887";
zsxq_access_token="0CBBBCD4-1A68-0BD3-AD93-124745DB5887";

"""测试获取主题"""
# headers = {
#     'Connection':'close',
#     'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
#     'cookie': "UM_distinctid=%s; _uab_collina=%s;name=%s;upload_channel=%s;user_id=%s;ws_address=%s;zsxq_access_token=%s;"%(UM_distinctid,_uab_collina,name,upload_channel,user_id,ws_address,zsxq_access_token)
# }

headers = {
    'Connection':'close',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    'cookie': "zsxq_access_token=%s;"%(zsxq_access_token)
}


wk_options = {
        "user-style-sheet": "temp.css",
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


{
'Host':"api.zsxq.com",
'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
'Accept':"application/json, text/plain, */*",
'Accept-Language':"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
'Accept-Encoding':"gzip, deflate, br",
'X-Request-Id':"5def8ee9b-890b-3826-d57b-54c5bda89f2",
'X-Version':"1.10.17",
'X-Signature':"5fca3c18b67e63f2a83053a5577daeb435aae6b0",
'X-Timestamp':"1568256940",
'Origin':"https://wx.zsxq.com",
'Connection':"keep-alive",
'Referer':"https://wx.zsxq.com/dweb2/index/group/455488242588",
'Cookie':"UM_distinctid=16cb2da72810-0e3b3efa303afb8-4c312272-1fa400-16cb2da728281; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216cb3667144547-0ecc86e2402a85-4c312272-2073600-16cb36671454c1%22%2C%22%24device_id%22%3A%2216cb3667144547-0ecc86e2402a85-4c312272-2073600-16cb36671454c1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; zsxq_access_token=0CBBBCD4-1A68-0BD3-AD93-124745DB5887; abtest_env=product"
}
