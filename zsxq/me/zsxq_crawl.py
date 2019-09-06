import re
import requests
import json
import os
import pdfkit
import shutil
import datetime
import urllib.request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import unquote
import random
import pandas as pd
import crawler.zsxq.me.sc_config as config
import crawler.zsxq.me.pdf_add_water as wt
import time
import fitz
import os
import PIL.Image as Image
class zsxq_crwal(object):
    """
    1、配置 headers
    2、wk_options
    3、topic配置 精华 问答 文件
    4、星主id
    """
    def __init__(self,topic_id_set:set=set(),file_id_set:set=set()):
        self.headers                    =config.headers
        self.wk_options                 =config.wk_options
        self.group_id                   =config.GROUP_ID
        self.late_time                  =int(datetime.datetime.strptime(config.NEW_LATE_DATE,'%Y-%m-%d %H:%M:%S').timestamp())*1000
        self.early_time                 =int(datetime.datetime.strptime(config.NEW_EARLY_DATE,'%Y-%m-%d %H:%M:%S').timestamp())*1000
        self.file_download_url          =config.FILE_DOWNLOAD_URL
        self.file_download_dir          =config.FILE_DOWNLOAD_DIR
        self.all_file_url               =config.ALL_FILE_URL
        self.file_id_set                =file_id_set
        self.topic_id_set               =topic_id_set
        self.data_dir                   =config.DATA_DIR
        self.data_root                  =config.DATA_ROOT
        self.topic_save_file            =config.TOPIC_SAVE_FILE
        self.topic_file_save_file       =config.TOPIC_FILE_SAVE_FILE
        self.file_name                  =config.FILE_NAME
        self.dowload_files              =config.DOWLOAD_FILES
        self.dowload_pics               =config.DOWLOAD_PICS
        self.dowload_comments           =config.DOWLOAD_COMMENTS
        self.only_digests               =config.ONLY_DIGESTS
        self.from_date_to_date          =config.FROM_DATE_TO_DATE
        self.delete_pics_when_done      =config.DELETE_PICS_WHEN_DONE
        self.delete_html_when_done      =config.DELETE_HTML_WHEN_DONE
        self.counts_per_time            =config.COUNTS_PER_TIME
        self.debug                      =config.DEBUG
        self.debug_num                  =config.DEBUG_NUM
        self.columns                    =config.COLUMNS
        self.download_file_columns      =config.DOWNLOAD_FILE_COLUMNS
        self.path_wk                    =config.PATH_WK
        self.digests_url                = config.DIGESTS_URL
        self.all_comtent_url            = config.ALL_COMTENT_URL
        self.topic_url                  = config.TOPIC_URL
        self.debug_num                  =1
        self.html_template              =config.html_template
        self.quetions_htmls             =[]
        self.digests_htmls             =[]
        self.num=1

    def _initDir_(self):
        # 初始化数据目录
        self.images_path = r'%s/images' % (self.data_dir)
        self.htmls_path = r'%s/htmls' % (self.data_dir)
        # self.files_path = r'%s/files' % (self.data_dir)
        # 初始化数据目录
        if not os.path.exists((self.data_dir)):
            os.makedirs( (self.data_dir))
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)
        #     html目录判断
        if not os.path.exists(self.htmls_path):
            os.makedirs(self.htmls_path)
        # if not os.path.exists(self.files_path):
        #     os.makedirs(self.files_path)
    def log(self,*args):
        ' 自定义log函数 '
        log_str=u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), args)
        print(log_str)

        with open('%s/%s.log' % (str(self.data_dir), str(int(time.strftime('%Y%m%d')))), 'a', encoding='utf-8') as f:
            f.write(log_str + "\n")

    # 获取文件id后下载文件（zip,doc,xls  ....）
    def get_gobal_file(self, file_name, file_url):
        savepath = r'%s/' % (self.file_download_dir)

        def reporthook(a, b, c):
            print("\r  Downloading: %5.1f%%" % (a * b * 100.0 / c), end="")

        filename =os.path.basename(file_name)
        if not os.path.isfile(os.path.join(savepath, filename)):
            # #对URL发起get请求获取页面内容
            response = requests.request("GET", file_url, headers=self.headers)
            # 将json对象转化为python对象
            jsonobj = json.loads(response.text)
            sleepTime = random.randint(3, 5)
            print("休眠时间", sleepTime)
            print('Downloading data from %s' % jsonobj['resp_data']['download_url'])
            urlretrieve(jsonobj['resp_data']['download_url'], os.path.join(savepath, filename), reporthook=reporthook)
            print('\nDownloading finished')
        else:
            print('File already exists!')

        # filesize = os.path.getsize(os.path.join(savepath, filename))
        #
        # print('File size = %.2f Mb' % (filesize / 1024 / 1024))
        # print(args)


        # print(args)
    def data2excel(self,df):
        df.set_index(['NUM'], inplace=True)
        df.to_excel('%s/topics.xlsx' % (self.data_dir), encoding='utf-8')
        df.drop('主题ID', axis=1, inplace=True)
        df.drop('阅读数', axis=1, inplace=True)
        df.drop('是否问答', axis=1, inplace=True)
        df.drop('是否文件', axis=1, inplace=True)
        df.to_excel('%s/微信（xumajie1688）_%s.xlsx' % (self.data_dir,time.strftime('%Y%m%d')), encoding='utf-8')
        self.log("导入excel完成！！！")
    def get_topic_list(self, endtime=None):
        self._initDir_()
        if not endtime:endtime=self.late_time
        if endtime<self.early_time:return
        start_url = self.topic_url % (str(self.group_id), str(self.counts_per_time), str(quote(get_urlcode_time(endtime))))
        self.log("开始请求", start_url)
        rsp = None
        try:
            rsp = requests.get(start_url, headers=self.headers)
        except Exception as e:

            self.log(e)
            time.sleep(5)
            rsp = requests.get(start_url, headers=self.headers)
        self.log("完成请求", start_url)
        with open('%s/%s.log' % (str(self.data_dir),str(int(time.strftime('%Y%m%d')))), 'a', encoding='utf-8') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+start_url + "\n")
        with open('temp.json', 'w', encoding='utf-8') as f:  # 将返回数据写入temp.json方便查看
            f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))
        if not json.loads(rsp.text).get('resp_data'): return
        for topic in json.loads(rsp.text).get('resp_data').get('topics'):
            tp = Topic(topic, self)
            topic_id = topic.get('topic_id')
            content = tp.getContent()
            author = tp.getAuthor()
            if int(topic.get('comments_count')) > 30:
                self.log("调试评论数",topic_id)
            cretime = (topic.get('create_time')[:23]).replace('T', ' ')
            """点赞数  评论数 回复数 阅读数"""
            index_tag = "点赞数:%s,评论数:%s,回复数:%s,阅读数:%s" % (
                str(topic.get('likes_count')), str(topic.get('comments_count')), str(topic.get('rewards_count')),
                str(topic.get('reading_count')))
            text = content.get('text', '')
            # text = handle_link(text)
            text = tp.handle_link(text)
            title = str(self.num) + '_' + cretime[:16] + '_' + tp.handle_link_tags()
            title=unquote(title)
            title=unquote(title)
            if topic.get('digested') == True:
                title += '_精华'

            if self.dowload_pics  and content.get('images'):
                soup = BeautifulSoup(self.html_template, 'html.parser')
                images_index = 0
                for img in content.get('images'):
                    url = img.get('large').get('url')
                    # local_url = './images/' + str(num - 1) + '_' + str(images_index) + '.jpg'
                    local_url = '%s/%s_%s.jpg' % (str(self.images_path), str(topic_id), str(images_index))
                    html_img_url = '../images/%s_%s.jpg' % (str(topic_id), str(images_index))
                    images_index += 1
                    urllib.request.urlretrieve(url, local_url)
                    img_p=soup.new_tag('p')
                    img_tag = soup.new_tag('img', src=html_img_url)
                    img_p.append(img_tag)
                    soup.body.append(img_p)
                html_img = str(soup)
                html = html_img.format(title=title, text=text, author=author, cretime=cretime, index_tag=index_tag)
            else:
                html = self.html_template.format(title=title, text=text, author=author, cretime=cretime,index_tag=index_tag)

            html = tp.getQuetions(html)

            html = tp.getFiles(html, None)
            comments = topic.get('show_comments')

            if self.dowload_comments and comments:
                topic_comment_url = self.all_comtent_url
                # topic_comment_url = 'https://api.zsxq.com/v1.10/topics/%s/comments?count=30&sort=asc'
                tp.get_topic_comment()
            soup_c = BeautifulSoup(html, 'html.parser')
            comment_hr = soup_c.new_tag('hr')
            for c in tp.conments:
                comment_p=soup_c.new_tag('p')
                soup_temp1=BeautifulSoup(c,'html.parser')
                comment_p.append(soup_temp1)
                comment_hr.append(comment_p)
            soup_c.body.append(comment_hr)
            html=str(soup_c)
            local_link = '=HYPERLINK("./htmls/%s.html")' % (str(topic.get('topic_id')))
            row = [str(self.num),local_link,str(topic.get('topic_id')), unquote(tp.handle_link_tags()), cretime[:16], tp.getAuthor(),
                   topic.get('reading_count'), topic.get('likes_count'), topic.get('comments_count'),
                   topic.get('rewards_count'), tp.get_digested(), tp.isQuetionStr(), tp.getIsFileTopicStr(),
                   tp.handle_link()[:200]]
# COLUMNS = ['html_url', '主题ID', '主题标签', '创建时间', '作者', '阅读数', '点赞数', '评论数', '回复数', '是否精华', '是否问答', '是否文件','主题内容']  # 主题字段
            pd.DataFrame([row],columns=self.columns).to_csv('%s/topics.csv' % (self.data_dir), mode='a', encoding='utf-8'
                                                            ,header=not os.path.exists('%s/topics.csv' % (self.data_dir)))

            #     写html
            file_path = r"%s/%s.html" % (str(self.htmls_path), str(topic.get('topic_id')))
            if html == None: break
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            # rows.append(row)
            if tp.isQuetion:
                self.quetions_htmls.append(html)
                #     写html
                fqa_path = r"%s/qa_%s.html" % (str(self.htmls_path), str(topic.get('topic_id')))
                with open(fqa_path, "w", encoding="utf-8") as f:
                    f.write(html)
            if topic.get('digested'):
                self.digests_htmls.append(html)
                fdigested_path = r"%s/digested_%s.html" % (str(self.htmls_path), str(topic.get('topic_id')))
                with open(fdigested_path, "w", encoding="utf-8") as f:
                    f.write(html)
            #     记录一些tipicId
            topicIds_file = r"%s/topic_ids" % (str(self.data_dir))
            with open(topicIds_file, "a", encoding="utf-8") as f:
                f.write(',' + str(topic.get('topic_id')))
            self.num += 1


        next_page = rsp.json().get('resp_data').get('topics')
        if next_page:
            end_time = get_time(next_page[-1]['create_time'])-1
            # next_url =url
            # print(next_url)
            self.get_topic_list(end_time)

    def get_near_3days_topics(self):
        # topic_ids=get_exists_topic_ids()
        self.dowload_files=True
        end_time = int(datetime.datetime.now().timestamp()*1000)
        start_time = int(datetime.datetime.now().timestamp() - 3 * 24 * 60 * 60)*1000
        end_dt = datetime.datetime.fromtimestamp(end_time/1000).strftime('%Y-%m-%d %H:%M:%S')
        self.data_dir = '%s/%s-3'%(self.data_root,end_dt[0:10].replace('-',''))
        self.late_time=end_time
        self.early_time=start_time
        self.get_topic_list(self.late_time)
        self.general_long_img()
        self.move_logfile()
    def get_near_ndays_topics(self,n):
        # topic_ids=get_exists_topic_ids()
        self.dowload_files=True
        end_time = int(datetime.datetime.now().timestamp()*1000)
        start_time = int(datetime.datetime.now().timestamp() - int(n) * 24 * 60 * 60)*1000
        end_dt = datetime.datetime.fromtimestamp(end_time/1000).strftime('%Y-%m-%d %H:%M:%S')
        self.data_dir = '%s/%s-%s'%(self.data_root,end_dt[0:10].replace('-',''),str(n))
        self.late_time=end_time
        self.early_time=start_time
        self.get_topic_list(self.late_time)
        self.reed_csv_and_make_pdf('是否问答', '是', '所有贴', all=True)
        self.general_long_img()
        self.move_logfile()
        # self.reed_csv_and_make_pdf('是否问答', '是', '问答')
        # self.reed_csv_and_make_pdf('是否精华', '是', '精华')



    def reed_csv_and_make_pdf(self,item_name='是否精华',condition='是',file_name='精华',all=None):
        # print(config.DATA_DIR)

        csv = pd.read_csv(open('%s/topics.csv'%(self.data_dir),encoding='utf-8'), index_col=None, header=0,lineterminator='\n',names=self.columns)
        df = pd.DataFrame(csv)
        # df.index = [i for i in range(len(df.get('主题ID')))]
        # df.set_index(['NUM'],inplace=True)

        # self.data2excel(df)
        if not all:
            df1=df[df[item_name] == condition]
        else:
            df1=df
        htmls = [ '%s/htmls/%s.html'%(self.data_dir,str('{:.0f}'.format(df1.get('主题ID').iloc[i]))) for i in range(len(df1.get('主题ID')))
                  if os.path.exists('%s/htmls/%s.html'%(self.data_dir,str('{:.0f}'.format(df1.get('主题ID').iloc[i]))))]
        print(htmls[0:2])
        if not os.path.exists('%s/topics.xlsx'%(self.data_dir)):
            self.data2excel(df)
            os.remove('%s/topics.xlsx'%(self.data_dir))
        try:
            # path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # wkhtmltopdf安装位置
            config_wk = pdfkit.configuration(wkhtmltopdf=self.path_wk)
            for i in range(0,len(htmls),500):
                start=i
                end=start+500
                if end > len(htmls)-1:
                    end=len(htmls)
                pdfkit.from_file(htmls[start:end], r"%s/%s_%s[%s-%s].pdf"%(str(self.data_dir),str(self.file_name),str(file_name),str(start+1),str(end)),
                                 options=self.wk_options,configuration=config_wk)
                input_pdf=r"%s/%s_%s[%s-%s].pdf" % (str(self.data_dir), str(self.file_name), str(file_name), str(start + 1), str(end))
                output=r"%s/微信（xumajie1688）%s[%s].pdf" % (str(self.data_dir), str(self.file_name), str(time.strftime('%Y%m%d')))
                wt.add_watermark(input_pdf=input_pdf,output=output, watermark='mark.pdf')
                os.remove(input_pdf)

        except Exception as e:
            self.log(e)
            pass
    def general_long_img(self):
        input = r"%s/微信（xumajie1688）%s[%s].pdf" % (str(self.data_dir), str(self.file_name), str(time.strftime('%Y%m%d')))
        input_dir = r"%s/微信（xumajie1688）%s[%s]" % (str(self.data_dir), str(self.file_name), str(time.strftime('%Y%m%d')))
        pdf_image(input,10)
        image_compose(input_dir,input_dir+'.png')
        shutil.rmtree(input_dir)
    def move_logfile(self):
        log_dir=os.path.dirname(self.data_dir)
        log_file=r'%s/%s.log'%(self.data_dir,str(time.strftime('%Y%m%d')))
        if os.path.exists(log_file):
            dist=r'%s/logs/%s.log'%(log_dir,str(time.strftime('%Y%m%d')))
            shutil.copyfile(log_file,dist)
            os.remove(log_file)
        topics_file = r'%s/topics.csv' % (self.data_dir)
        if os.path.exists(topics_file):
            topics_dist = r'%s/logs/%s-topics.csv' % (log_dir,str(time.strftime('%Y%m%d')))
            shutil.copyfile(topics_file, topics_dist)
            os.remove(topics_file)
        topics_id_file = r'%s/topic_ids' % (self.data_dir)
        if os.path.exists(topics_id_file):
            topics_id_dist = r'%s/logs/%s-topic_ids' % (log_dir, str(time.strftime('%Y%m%d')))
            shutil.copyfile(topics_id_file, topics_id_dist)
            os.remove(topics_id_file)
    def get_file_list(self,endtime=None):

        if not os.path.exists(self.file_download_dir):
            os.makedirs(self.file_download_dir)
        if not endtime: endtime = self.late_time
        if endtime < self.early_time: return
        start_url = self.all_file_url % (
        str(self.group_id), str(self.counts_per_time), str(quote(get_urlcode_time(endtime))))
        self.log("开始请求", start_url)
        rsp = None
        try:
            rsp = requests.get(start_url, headers=self.headers)
        except Exception as e:


            self.log(e)
            time.sleep(5)
            rsp = requests.get(start_url, headers=self.headers)
        self.log("完成请求", start_url)

        # with open('%s/%s.log' % (str(self.data_dir), str(int(time.strftime('%Y%m%d')))), 'a', encoding='utf-8') as f:
        #     f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\t' + start_url + "\n")
        with open('temp.json', 'w', encoding='utf-8') as f:  # 将返回数据写入temp.json方便查看
            f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))
        if not json.loads(rsp.text).get('resp_data'): return
        for f in json.loads(rsp.text).get('resp_data').get('files'):
            # "file": {
            #     "file_id": 51184452822424,
            #     "name": "生财有术武汉站.pptx",
            #     "hash": "129148c1f692c7b8db3cb5d93634bcfc53da9b99f041c86a5cafbbe99f41cd49",
            #     "size": 3582302,
            #     "download_count": 192,
            #     "create_time": "2019-05-29T01:50:27.612+0800",
            #     "duration": 0
            # }
            file=f['file']
            file_id=file['file_id']
            file_name=file['name']
            file_local_name=validateTitle(file_name)
            file_size='%.2fM'%(file['size']/(1024*1024))
            file_download_count=file['download_count']
            file_create_time=str(file['create_time']).split('.')[0].replace('T',' ')
            topic=f['topic']
            file_topic_id=topic['topic_id']
            goup_id=self.group_id
            # [ '文件名称','主题ID', '文件ID', '创建时间',  '下载数', '文件大小','本地文件名称']
            row = [str(file_name),str(file_topic_id), str(file_id), str(file_create_time), str(file_download_count),str(file_size),str(file_local_name)]
            if  file_id in self.file_id_set:
                continue
            pd.DataFrame([row], columns=self.download_file_columns).to_csv('%s/file_topic.csv' % (self.data_root), mode='a',
                                                             encoding='utf-8', header=not os.path.exists('%s/file_topic.csv' % (self.data_root)))
            file_url = self.file_download_url % (str(file_id))
            self.get_gobal_file(file_local_name,file_url)
        next_page = rsp.json().get('resp_data').get('files')
        if next_page:
            end_time = get_time(next_page[-1]['file']['create_time']) - 1
            self.get_file_list(end_time)
class Topic(object):
    def __init__(self, topic_js,zc:zsxq_crwal):
        self.topic_js = topic_js
        self.isQuetion=False
        self.isFileTopic=False
        self.zc=zc
        self.conments=[]


    def getContent(self):
        text=''
        if self.topic_js.get('question'):
            self.text = self.topic_js.get('question')
        elif self.topic_js.get('talk'):
            self.text = self.topic_js.get('talk')
        elif self.topic_js.get('task'):
            self.text = self.topic_js.get('task')
        else:
            self.text = self.topic_js.get('solution')
        return self.text
    def handle_link_tags(self):
        text = self.getContent().get('text','')
        soup = BeautifulSoup(text, "html.parser")
        mention = soup.find_all('e', attrs={'type': 'mention'})
        tags_str = ''
        if len(mention):
            for m in mention:
                mention_name = m.attrs['title']
                new_tag = soup.new_tag('span')
                new_tag.string = mention_name
                m.replace_with(new_tag)
                tags_str += mention_name

        hashtag = soup.find_all('e', attrs={'type': 'hashtag'})
        if len(hashtag):
            for tag in hashtag:
                tag_name = unquote(tag.attrs['title'])
                new_tag = soup.new_tag('span')
                new_tag.string = tag_name
                tag.replace_with(new_tag)
                tags_str += tag_name

        links = soup.find_all('e', attrs={'type': 'web'})
        if len(links):
            for link in links:
                title = unquote(link.attrs['title'])
                href = unquote(link.attrs['href'])
                new_a_tag = soup.new_tag('a', href=href)
                new_a_tag.string = title
                link.replace_with(new_a_tag)
                tags_str += title
        return tags_str

    def handle_link(self,text=None):
        if text:
            text=text
        else:
            text=self.getContent().get('text','')

        soup = BeautifulSoup(text, "html.parser")
        mention = soup.find_all('e', attrs={'type': 'mention'})
        if len(mention):
            for m in mention:
                mention_name = m.attrs['title']
                new_tag = soup.new_tag('span')
                new_tag.string = mention_name
                m.replace_with(new_tag)

        hashtag = soup.find_all('e', attrs={'type': 'hashtag'})
        if len(hashtag):
            for tag in hashtag:
                tag_name = unquote(tag.attrs['title'])
                new_tag = soup.new_tag('span')
                new_tag.string = tag_name
                tag.replace_with(new_tag)

        links = soup.find_all('e', attrs={'type': 'web'})
        if len(links):
            for link in links:
                title = unquote(link.attrs['title'])
                href = unquote(link.attrs['href'])
                new_a_tag = soup.new_tag('a', href=href)
                new_a_tag.string = title
                link.replace_with(new_a_tag)

        text = str(soup)
        text = re.sub(r'<e[^>]*>', '', text).strip()
        text = text.replace('\n', '<br>')
        return text

    def handle_link(self,text=None):
        if text:
            text=text
        else:
            text=self.getContent().get('text','')

        soup = BeautifulSoup(text, "html.parser")
        mention = soup.find_all('e', attrs={'type': 'mention'})
        if len(mention):
            for m in mention:
                mention_name = m.attrs['title']
                new_tag = soup.new_tag('span')
                new_tag.string = mention_name
                m.replace_with(new_tag)

        hashtag = soup.find_all('e', attrs={'type': 'hashtag'})
        if len(hashtag):
            for tag in hashtag:
                tag_name = unquote(tag.attrs['title'])
                new_tag = soup.new_tag('span')
                new_tag.string = tag_name
                tag.replace_with(new_tag)

        links = soup.find_all('e', attrs={'type': 'web'})
        if len(links):
            for link in links:
                title = unquote(link.attrs['title'])
                href = unquote(link.attrs['href'])
                new_a_tag = soup.new_tag('a', href=href)
                new_a_tag.string = title
                link.replace_with(new_a_tag)

        text = str(soup)
        text = re.sub(r'<e[^>]*>', '', text).strip()
        text = text.replace('\n', '<br>')
        return text

    def getAuthor(self):
        content =self.getContent()
        anonymous = content.get('anonymous')
        if anonymous:
            author = '匿名用户'
        else:
            author = content.get('owner').get('name')
        return author

    def get_digested(self):
        topic = self.topic_js
        if topic.get('digested'):
            return '是'
        else:
            return '否'
    def isQuetionStr(self):
        if self.isQuetion:
            return '是'
        else:
            return '否'
    def getIsFileTopicStr(self):
        if self.isFileTopic:
            return '是'
        else:
            return '否'
    def get_topic_comment(self,begin_time=None):
        topic_id=self.topic_js.get('topic_id')
        t_c_time=get_time(self.topic_js.get('create_time'))
        # comment_url = 'https://api.zsxq.com/v1.10/topics/%s/comments?count=30&sort=asc' % (str(topic_id))
        # ALL_COMTENT_URL = 'https://api.zsxq.com/v1.10/topics/%s/comments?count=%s&sort=asc&begin_time=%s'
        if not begin_time:
            begin_time=t_c_time
        comment_url = self.zc.all_comtent_url % (str(topic_id),str(self.zc.counts_per_time),quote(str(get_urlcode_time(begin_time))))
        # print(printTime(), "开始下载", comment_url)
        rsp=None
        ran_sec=random.randint(5,10)
        try:
            rsp = requests.get(comment_url, headers=self.zc.headers)
        except Exception as e:
            self.log(e)
            time.sleep(ran_sec)
            rsp = requests.get(comment_url, headers=self.zc.headers)
        # print(printTime(), "完成下载", comment_url)
        s = requests.session()
        s.keep_alive = False

        with open('temp.json', 'w', encoding='utf-8') as f:  # 将返回数据写入temp.json方便查看
            f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))

        # soup = BeautifulSoup(html, 'html.parser')
        # hr_tag = soup.new_tag('hr')
        if rsp==None or not json.loads(rsp.text).get('resp_data') or  not json.loads(rsp.text).get('resp_data').get('comments'):return

        for comment in json.loads(rsp.text).get('resp_data').get('comments'):
            replied_comment_str = ''
            replied_comments = comment.get('replied_comments')
            if replied_comments:
                for replied_comment in replied_comments:
                    replied_comment_str = '[' + replied_comment.get('owner').get(
                        'name') + ' 回复 ' + replied_comment.get('repliee').get(
                        'name') + '] : ' + self.handle_link(replied_comment.get('text'))
                    self.conments.append(replied_comment_str)
            else:
                replied_comment_str = '[' + comment.get('owner').get('name') + '] : ' + comment.get('text')
                self.conments.append(replied_comment_str)
            # comment_tag1 = soup.new_tag('p')
            # soup_temp1 = BeautifulSoup(replied_comment_str, 'html.parser')
            # comment_tag1.append(soup_temp1)
            # hr_tag.append(comment_tag1)
            replied_comment_str='<p>%s</p>'%(replied_comment_str)
        # soup.body.append(hr_tag)
        if json.loads(rsp.text).get('resp_data').get('comments'):
            next_btime =json.loads(rsp.text).get('resp_data').get('comments')[-1]['create_time']
            self.get_topic_comment(get_time(next_btime)+1)
    def getFiles(self,html,content):
        if content:
            content=content
        else:
            content=self.getContent()
        files = content.get('files')
        if files:
            self.isFileTopic=True
            files_content = '<i>文件列表(需访问网站下载) :<br>'
            for f in files:
                files_content += f.get('name') + '<br>'
                if self.zc.dowload_files==False:continue
                try:
                    # if(file_id==0):
                    #     query_current_time=f.get('create_time')
                    file_url = self.zc.file_download_url%(str(f.get('file_id')))
                    print(file_url)
                    file_name = f.get('name')
                    local_file=validateTitle(file_name)
                    create_time =str.replace(f.get('create_time'), '-', '').replace('T','').replace( ':', '').split('.')[0]
                    download_count = f.get('download_count')
                    data_file_id = f.get('file_id')
                    size = '%.2fM' % (f.get('size') / 1024 / 1024)
                    self.zc.get_gobal_file(local_file,file_url)
                    self.zc.log(data_file_id, file_name, download_count, create_time, size)
                    if data_file_id not in self.zc.file_id_set:
                        self.zc.file_id_set.add(data_file_id)
                        # ['主题ID', '文件ID', '星球号', '创建时间', '作者', '下载数', '文件大小', '文件名称']  #
                        # ['文件名称', '主题ID', '文件ID', '创建时间','作者', '下载数', '文件大小', '本地文件名称']
                        row=[file_name,self.topic_js.get('topic_id'),data_file_id,create_time,self.getAuthor(),download_count,size,local_file]
                        file_path='%s/'%(self.zc.file_download_dir)
                        pd.DataFrame(data=[row],columns=self.zc.download_file_columns).to_csv(file_path,mode='a',encoding='utf-8',header=not os.path.exists(file_path))
                except IOError as e:
                    self.zc.log(e)
                    print('Not have any files!')


            files_content += '</i>'
            soup = BeautifulSoup(html, 'html.parser')
            files_tag = soup.new_tag('p')
            soup_temp = BeautifulSoup(files_content, 'html.parser')
            files_tag.append(soup_temp)
            soup.body.append(files_tag)
            html = str(soup)
        return html
    def getQuetions(self,html=None):
        if self.topic_js.get('question'):
            self.isQuetion = True
            answer_author = self.topic_js.get('answer').get('owner').get('name', '')
            answer = self.topic_js.get('answer').get('text', "")
            # answer = handle_link(answer)
            answer = self.handle_link(answer)

            soup = BeautifulSoup(html, 'html.parser')
            answer_tag = soup.new_tag('p')

            answer = '【' + answer_author + '】 回答：<br>' + answer
            soup_temp = BeautifulSoup(answer, 'html.parser')
            answer_tag.append(soup_temp)
            soup.body.append(answer_tag)
            html = str(soup)
        return html

# 获取已经下载的文件id列表
def get_file_id_set(file_path=None,column='主题ID'):
    if not os.path.exists(file_path):return set()
    # df=pd.DataFrame(pd.read_csv(file_path,encoding='utf-8',lineterminator='\n',names=config.COLUMNS,header=0))
    df=pd.read_csv(open(file_path,encoding='utf-8'),encoding='utf-8',lineterminator='\n',names=config.COLUMNS,header=0)
    return set(df.get(column))
def get_urlcode_time(t):
    return datetime.datetime.fromtimestamp(t/1000).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+0800'
def get_time(dt):
    return int(datetime.datetime.strptime(dt.split('+')[0].replace('T',' '),'%Y-%m-%d %H:%M:%S.%f').timestamp()*1000)
def reed_csv_and_make_pdf(item_name='是否精华',condition='是',file_name='精华',all=None):
    # print(config.DATA_DIR)
    csv = pd.read_csv('%s/topics.csv'%(config.DATA_DIR),encoding='utf-8', index_col=None, header=0,lineterminator='\n',names=config.COLUMNS)
    df = pd.DataFrame(csv)
    if not all:
        df1=df[df[item_name] == condition]
    else:
        df1=df
    htmls = [ '%s/htmls/%s.html'%(config.DATA_DIR,str(df1.get('主题ID').iloc[i])) for i in range(len(df1.get('主题ID')))
              if os.path.exists('%s/htmls/%s.html'%(config.DATA_DIR,str(df1.get('主题ID').iloc[i])))]
    print(htmls[0:2])
    df1.to_excel('%s/topics_1.xlsx' % (config.DATA_DIR), encoding='utf-8')
    try:
        # path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # wkhtmltopdf安装位置
        config_wk = pdfkit.configuration(wkhtmltopdf=config.PATH_WK)
        for i in range(0,len(htmls),1000):
            start=i
            end=start+500
            if end > len(htmls)-1:
                end=len(htmls)
            pdfkit.from_file(htmls[start:end], r"%s/%s_%s[%s-%s].pdf"%(str(config.DATA_DIR),str(config.FILE_NAME),str(file_name),str(start+1),str(end)), options=config.wk_options,configuration=config_wk)
    except Exception as e:
        print(e)
        pass
def add_ptag_css(html_path=None):
    if not os.path.exists(r'%s/htmls_new/'%(config.DATA_DIR)):
        os.makedirs(r'%s/htmls_new/'%(config.DATA_DIR))
    for f1 in os.listdir(r'%s/htmls/'%(config.DATA_DIR)):
        with open(r'%s/htmls/%s'%(config.DATA_DIR,f1), 'r', encoding='utf-8') as f:
            html = f.read()
            soup =BeautifulSoup(html,'html.parser')
            head = soup.select('head')[0]
            style = soup.new_tag('style')
            style['type'] = 'text/css'
            style.string = 'p {width: 40%;}'
            head.append(style)

        with open(r'%s/htmls_new/%s'%(config.DATA_DIR,f1), 'w', encoding='utf-8') as f2:
            f2.write(str(soup))


    # pd.DataFrame().to_html()
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def get_dir_name(file_dir):
    base_name = os.path.basename(file_dir)  # 获得地址的文件名
    dir_name = os.path.dirname(file_dir)  # 获得地址的父链接
    return dir_name, base_name
def pdf_image(pdf_name,pageCount=None):
    dir_name, base_name = get_dir_name(pdf_name)
    pdf = fitz.Document(pdf_name)
    if not pageCount:
        pageCount=pdf.pageCount
    for pg in range(0, pageCount):
        page = pdf[pg]  # 获得每一页的对象
        trans = fitz.Matrix(1.0, 1.0).preRotate(0)
        pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
        save_dir=dir_name + os.sep + base_name[:-4]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        pm.writePNG(save_dir+ os.sep + '{:0>3d}.png'.format(pg + 1))  # 保存图片
    pdf.close()
# 定义图像拼接函数 长图
def image_compose(images_path,image_save_path,image_size=512):
    listdir = [i for i in os.listdir(images_path)]
    image_row=len(listdir)
    image_column=1
    to_image = Image.new('RGB', (image_column * image_size, image_row * image_size))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):
            # from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            from_image = Image.open(images_path + os.sep+listdir[image_column * (y - 1) + x - 1]).resize((image_size, image_size), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * image_size, (y - 1) * image_size))
    return to_image.save(image_save_path)  # 保存新图
if __name__ == '__main__':
    # zc=zsxq_crwal()
    # zc.log(zc.early_time,zc.late_time)
    # end_time=get_url_end_time(int(datetime.datetime.strptime(config.NEW_LATE_DATE,'%Y-%m-%d %H:%M:%S').timestamp()))
    # print(end_time)
    # print(time.strftime('%Y%m%d'))
    # print(get_time('2019-08-28T17:52:26.806+0800'))
    # print(get_urlcode_time(get_time('2019-08-28T17:52:26.806+0800')))
    # print(zc.headers)
    # print('2019-08-28T17:52:26.806+0800'[0:10].replace('-',''))
    # config.DATA_DIR = './ALL-20190829'
    topic_id_set=get_file_id_set('%s/%s'%(config.DATA_ROOT,str(config.TOPIC_SAVE_FILE)),'主题ID')
    file_id_set=get_file_id_set('%s/%s'%(config.FILE_DOWNLOAD_DIR,str(config.TOPIC_FILE_SAVE_FILE)),'文件ID')
    zc = zsxq_crwal(topic_id_set,file_id_set)

    # df = pd.read_csv(open(r'F:/知识星球/生财有术/ALL-20190829/topics.csv', encoding='utf-8'), index_col=None, header=0,
    #                   lineterminator='\n', names=config.COLUMNS)
    # df.to_excel(r'F:/知识星球/生财有术/ALL-20190829/(微信：xumajie1688)生财有术.xlsx', encoding='utf-8')

    # zc = zsxq_crwal()
    # zc.data_dir=r'F:/知识星球/生财有术/20190904-2'
    # zc.general_long_img()
    # zc.get_file_list()
    # zc.get_near_3days_topics()
    # zc.data_dir='./ALL-20190829'
    # zc.get_topic_list(zc.late_time)
    zc.get_near_ndays_topics(2)

    # zc.data_dir = r'F:/知识星球/生财有术/20190904-1'
    # zc.move_logfile()
    # zc.reed_csv_and_make_pdf('是否问答','是','所有贴',all=True)
    # zc.reed_csv_and_make_pdf('是否问答','是','问答')
    # zc.reed_csv_and_make_pdf('是否精华','是','精华')

    # reed_csv_and_make_pdf('是否问答','是','所有贴',all=True)
