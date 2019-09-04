from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import datetime
import os
import shutil
# 生成水印PDF 水印工具
def add_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)
    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()
     # 给所有页面添加水印
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)
    with open(output, 'wb') as out:
         pdf_writer.write(out)


def create_watermark(content):
    #默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    c = canvas.Canvas(file_name, pagesize = (30*cm, 30*cm))
    #移动坐标原点(坐标系左下为(0,0))
    c.translate(10*cm, 5*cm)
    #设置字体
    c.setFont("Helvetica", 80)
    #指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    #指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    #画一个矩形
    # c.rect(cm, cm, 7*cm, 17*cm, fill=1)
    #旋转45度,坐标系被旋转
    c.rotate(45)
    #指定填充颜色
    c.setFillColorRGB(0.6, 0, 0)
    #设置透明度,1为不透明
    c.setFillAlpha(0.3)
    #画几个文本,注意坐标系旋转的影响
    c.drawString(3*cm, 0*cm, content)
    c.setFillAlpha(0.6)
    #关闭并保存pdf文件
    c.save()
    return file_name
def dateTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
if __name__ == '__main__':
    DIR=r'F:/知识星球/生财有术/20190829-7/'
    for f in os.listdir(DIR):
        if f.split(".")[-1]=="pdf" and f.find('xumajie1688')==-1 and f.find('mark.pdf')==-1 :
            print(dateTime(),"正在打水印",f)
            input_pdf=os.path.join(DIR,f)
            output=os.path.join(DIR,'微信（xumajie1688）%s'%(f))
            if os.path.exists(output):continue
            add_watermark(input_pdf=input_pdf,output=output, watermark='mark.pdf')
            os.remove(input_pdf)
            # shutil.rmtree(input_pdf)
    # add_watermark(input_pdf='./生财有术/20190821-20190823/生财有术_精华[0-1].pdf',output = './生财有术/20190821-20190823/生财有术_精华[vx：xumajie1688].pdf',watermark = 'mark.pdf')
    # create_watermark("vx:xumajie1688")