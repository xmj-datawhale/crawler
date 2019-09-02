NEW_LATE_DATE  = '2019-09-01 00:00:00' # 最晚时间
NEW_EARLY_DATE = '2017-03-17 00:00:00'# 最早时间
GROUP_ID = '1824528822'                                  # 知识星球中的小组ID
FILE_NAME               = '生财有术'                    # 生成文件的名字
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
DATA_DIR                =r'F:/知识星球/生财有术/20190829-7'
DATA_ROOT               =r'F:/知识星球/生财有术'
FILE_DOWNLOAD_DIR       = r'F:/知识星球/生财有术/ALL_FILE'
FILE_DOWNLOAD_URL       = 'https://api.zsxq.com/v1.10/files/%s/download_url'
ALL_FILE_URL            = 'https://api.zsxq.com/v1.10/groups/%s/files?count=%s&end_time=%s' # [end_time-1]'https://api.zsxq.com/v1.10/groups/1824528822/files?count=20&end_time=2019-06-13T16%3A19%3A29.514%2B0800'
COLUMNS                 = ['NUM','html_url', '主题ID', '主题标签', '创建时间','作者', '阅读数', '点赞数', '评论数', '回复数', '是否精华','是否问答', '是否文件','主题内容']#主题字段
DOWNLOAD_FILE_COLUMNS   = [ '文件名称','主题ID', '文件ID', '创建时间',  '下载数', '文件大小','本地文件名称']#主题下载字段

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

"""测试获取主题"""
headers = {
    'Connection':'close',
    'accept': "application/json, text/plain, */*",
    'origin': "https://wx.zsxq.com",
    'x-version': "1.10.14",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    'x-request-id': "99096A6A-AC87-4CC4-28CB-C240E4719F4B",
    'x-signature': "38cb64e03fdae4828b39432b374281d120c98e17",
    'referer': "https://wx.zsxq.com/dweb/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    'cookie': "UM_distinctid=16cb2da72810-0e3b3efa303afb8-4c312272-1fa400-16cb2da728281; \
        _uab_collina=156636875770574735449994;\
        name=sunny;\
        upload_channel=qiniu;\
        user_id=88511414142252;\
        ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3D99096A6A-AC87-4CC4-28CB-C240E4719F4B;\
        zsxq_access_token=99096A6A-AC87-4CC4-28CB-C240E4719F4B;"

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