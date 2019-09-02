import json
import re
from urllib import request
from urllib.request import urlretrieve
import os
from urllib.parse import quote
import requests
import time
from datetime import datetime, timedelta
import random

headers = {
    'accept': "application/json, text/plain, */*",
    'origin': "https://wx.zsxq.com",
    'x-version': "1.10.14",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    'x-request-id': "da7ddfcd-356d-c85b-5d1b-4d59933923c5",
    'referer': "https://wx.zsxq.com/dweb/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    # 'cookie': "zsxq_access_token=zsxq.py;UM_distinctid=16ca80bddd0383-0ecd3b4229e928-37c143e-1fa400-16ca80bddd1486;avatar_url=https%3A//images.zsxq.com/Fvv1wVWMXu_isO64oXhGYlmHoErr%3Fe%3D1906272000%26token%3DkIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD%3ATQapZjuttp1LcCGTVFlWFx6UJ_k%3D&name=%u661F%u671F%u516B&upload_channel=qiniu&user_id=548284811158524&ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3D42680B01-00F7-545C-DAE8-0E209D2D6C41&zsxq_access_token=42680B01-00F7-545C-DAE8-0E209D2D6C41",
  # 'cookie': "UM_distinctid=16c6ed8296f4ee-087749adad3d-36664c08-1fa400-16c6ed8297122; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c92fd13ba45b-0a0bae5b564ac-36664c08-2073600-16c92fd13bc382%22%2C%22%24device_id%22%3A%2216c92fd13ba45b-0a0bae5b564ac-36664c08-2073600-16c92fd13bc382%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; zsxq_access_token=9C5814CB-E434-B07B-906B-CC569F795D75"
    'cookie': "UM_distinctid=16ca80bddd0383-0ecd3b4229e928-37c143e-1fa400-16ca80bddd1486; \
    _uab_collina=156620938101656747576869;\
    name=%u661F%u671F%u516B;\
    upload_channel=qiniu;\
    user_id=548284811158524;\
    ws_address=wss%3A//ws.zsxq.com/ws%3Fversion%3Dv1.10%26access_token%3D160885C8-993B-D0B5-BE18-F77560A7EFD6;\
    zsxq_access_token=160885C8-993B-D0B5-BE18-F77560A7EFD6;\
    avatar_url=https%3A//images.zsxq.com/Fvv1wVWMXu_isO64oXhGYlmHoErr%3Fe%3D1906272000%26token%3DkIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD%3ATQapZjuttp1LcCGTVFlWFx6UJ_k%3D;"

}

fileIds=[]
#加入的圈子id
def get_group(headers):
    url = "https://api.zsxq.com/v1.10/groups"
    #对URL发起get请求获取页面内容
    response = requests.request("GET",url,headers=headers)
    #将json对象转化为python对象
    jsonobj = json.loads(response.text)
    # print(jsonobj)
    # json1 = json.loads(jsonobj)
    # print(type(jsonobj))
    try:
        for number in range(len(jsonobj['resp_data']['preferences']['sorts'])):
            print("星球ID：",jsonobj['resp_data']['groups'][number]['group_id'])
            print("星球的名字：",jsonobj['resp_data']['groups'][number]['name'])
            print("星球的星主是：",jsonobj['resp_data']['groups'][number]['owner']['name'])
            print('\n')
    except Exception:
        print("已没有再多的星球")
    # print(type(jsonobj['resp_data']['preferences']['sorts']))
    # print(len(jsonobj['resp_data']['preferences']['sorts']))
    
#获取文件id后下载文件（zip,doc,xls  ....）
def get_gobal_file(file_url,file_name,headers,savepath='./'):
    # #对URL发起get请求获取页面内容
    response = requests.request("GET",file_url,headers=headers)
    #将json对象转化为python对象
    jsonobj = json.loads(response.text)
    # r = requests.get(jsonobj['resp_data']['download_url'])
    # with open(file_name,"wb") as f:
    #     f.write(r.content)
    # print(jsonobj)
    # print(jsonobj['resp_data']['download_url'])
    # with open(file_name,"wb") as f:
    #     f.write()
    # for download_url in jsonobj['resp_data']['download_url']:
    #     pass
    def reporthook(a, b, c):
        print("\r  Downloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    filename = os.path.basename(file_name)
    if not os.path.isfile(os.path.join(savepath, filename)):
        sleepTime = random.randint(3, 5)
        print("休眠时间", sleepTime)
        print('Downloading data from %s' % jsonobj['resp_data']['download_url'])
        urlretrieve(jsonobj['resp_data']['download_url'], os.path.join(savepath,filename), reporthook=reporthook)
        print('\nDownloading finished')
    else:
        print('File already exists!')

    filesize = os.path.getsize(os.path.join(savepath,filename))

    print('File size = %.2f Mb' % (filesize/1024/1024))

#生成时间对应的格式
def get_end_time():
    now = datetime.now()
    print(now)
    time1 = now.strftime('%Y-%m-%d')
    print(time1)
    time2 = now.strftime('%H:%M:%S')
    print(time2)
    number = str(random.randint(100,999))
    # print (type(random.randint(100,999)))
    end_time = time1+'T'+time2+'.'+number+'+0800'
    return end_time




#获取某个星球下的文件id
def get_download_url(headers,group_id):
    query_current_time='2019-05-18T23:12:11.300+0800'
    query_end_time='2019-08-19T17:17:14.799+0800'
    # url = "https://api.zsxq.com/v1.10/groups/"+group_id+"/files?count=3"
    end_time = get_end_time()
    savepath = './%s/' % (group_id)

    url = "https://api.zsxq.com/v1.10/groups/"+group_id+"/files?count=20&end_time="+quote(query_current_time)
    print(url)
    #对URL发起get请求获取页面内容
    response = requests.request("GET",url,headers=headers)
    jsonobj = json.loads(response.text)
    print(type(jsonobj))
    while query_end_time[:13] != query_current_time[:13]:
        # print(jsonobj['resp_data']['files'][0]['file']['file_id'])
        # print(len(jsonobj['resp_data']['files']))
        if os.path.exists(savepath)==False:
            os.mkdir(savepath)
        t1=int(datetime.strptime(query_current_time.replace('T',' ').split('.')[0],'%Y-%m-%d %H:%M:%S').timestamp())
        t2=int(datetime.strptime(end_time.replace('T',' ').split('.')[0],'%Y-%m-%d %H:%M:%S').timestamp())

        # if len(jsonobj['resp_data']['files']) ==0 and t2>t1:
        #     # 后移一天
        #     query_current_time=datetime.utcfromtimestamp(int(datetime.strptime(query_current_time.replace('T',' ').split('.')[0],'%Y-%m-%d %H:%M:%S').timestamp())+24 * 60 * 60).strftime('%Y-%m-%dT%H:%M:%S') + '.%d+0800' % (random.randint(100, 999))
            # query_current_time=str.replace(time.strftime("%Y-%m-%dT%H:%M:%S.R+0800", time.localtime(int(datetime.strptime('2019-04-16 23:12:11','%Y-%m-%d %H:%M:%S').timestamp())+24 * 60 * 60)),'R',str(random.randint(100,999)))
        for file_id in range(len(jsonobj['resp_data']['files'])):
            try:
                # if(file_id==0):
                #     query_current_time=jsonobj['resp_data']['files'][file_id]['file']['create_time']
                file_url = 'https://api.zsxq.com/v1.10/files/'+str(jsonobj['resp_data']['files'][file_id]['file']['file_id'])+'/download_url'
                print(file_url)
                file_name = jsonobj['resp_data']['files'][file_id]['file']['name']
                create_time=str.replace(jsonobj['resp_data']['files'][file_id]['file']['create_time'],'-','').replace('T','').replace(':','').split('.')[0]
                download_count=jsonobj['resp_data']['files'][file_id]['file']['download_count']
                data_file_id=jsonobj['resp_data']['files'][file_id]['file']['file_id']
                size='%.2fM'%(jsonobj['resp_data']['files'][file_id]['file']['size']/1024/1024)

                get_gobal_file(file_url,file_name,headers,savepath=savepath)
                print(data_file_id,file_name,download_count,create_time,size)
                if data_file_id not in fileIds:
                    fileIds.append(data_file_id)
                    file_write(file_name,file_url,create_time,download_count,size,group_id)
            except IOError as e:
                    print(e)
                    print('Not have any files!')
                    # 后移5天
        query_current_time = datetime.utcfromtimestamp(int(datetime.strptime(query_current_time.replace('T', ' ').split('.')[0],'%Y-%m-%d %H:%M:%S').timestamp()) + 10*24 * 60 * 60).strftime('%Y-%m-%dT%H:%M:%S') + '.%d+0800' % (random.randint(100, 999))
        url = "https://api.zsxq.com/v1.10/groups/" + group_id + "/files?count=20&end_time=" + quote(query_current_time)
        print(url)
        # 对URL发起get请求获取页面内容
        sleepTime=random.randint(5, 10)
        print("休眠时间",sleepTime)
        time.sleep(sleepTime)
        response = requests.request("GET", url, headers=headers)
        jsonobj = json.loads(response.text)

    

def file_write(file_name,file_url,create_time,download_count,size,group_id):
    try:
        f = open('./%d/log.txt'%(group_id),'a',encoding='utf-8')
        f.write(file_name+'\t'+str(create_time)+'\t'+str(download_count)+'\t'+str(size)+'\t'+'\n')
        f.write(file_url+'\n\n')
        f.close()
    except IOError as e:
        print('读写文件失败！')

# 144818158482
if __name__ == "__main__":
    get_group(headers)
    # get_gobal_file(headers)
    # group_id = input("请输入星球id：")
    group_id = 144818158482
    print("正在下载星球：")
    get_download_url(headers,group_id)
