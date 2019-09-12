from urllib.request import quote
NEW_LATE_DATE  = '2017-04-27 00:00:00' # 最晚时间
NEW_EARLY_DATE = '2017-03-05 00:00:00'# 最早时间
GROUP_ID = '8412585182'                                  # 知识星球中的小组ID
FILE_NAME               = '编码美丽'                    # 生成文件的名字
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
DATA_DIR                =r'F:/知识星球/编码美丽/ALL_DATA'
DATA_ROOT               =r'F:/知识星球/编码美丽'
FILE_DOWNLOAD_DIR       = r'F:/知识星球/编码美丽/ALL_FILE'
FILE_DOWNLOAD_URL       = 'https://api.zsxq.com/v1.10/files/%s/download_url'
ALL_FILE_URL            = 'https://api.zsxq.com/v1.10/groups/%s/files?count=%s&end_time=%s' # [end_time-1]'https://api.zsxq.com/v1.10/groups/8412585182/files?count=20&end_time=2019-06-13T16%3A19%3A29.514%2B0800'
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

UM_distinctid="6cb2da72810-0e3b3efa303afb8-4c312272-1fa400-16cb2da728281";
_uab_collina="156636875770574735449994";
name=quote("星期八");
upload_channel="qiniu";
user_id="15142221115542";
ws_address="wss://ws.zsxq.com/ws?version=v1.10&access_token=0CBBBCD4-1A68-0BD3-AD93-124745DB5887";
zsxq_access_token="0CBBBCD4-1A68-0BD3-AD93-124745DB5887";

headers = {
    'Connection':'close',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    'cookie': "UM_distinctid=%s; _uab_collina=%s;name=%s;upload_channel=%s;user_id=%s;ws_address=%s;zsxq_access_token=%s;"%(UM_distinctid,_uab_collina,name,upload_channel,user_id,ws_address,zsxq_access_token)
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