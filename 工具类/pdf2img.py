# -*- coding: utf-8 -*-
'''
https://www.qikqiak.com/post/python-convert-pdf-images/
'''
import fitz
import os

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
        pm.writePNG(dir_name + os.sep + base_name[:-4] + '_' + '{:0>3d}.png'.format(pg + 1))  # 保存图片
    pdf.close()
for i in range(10):
    pdf_image(r'F:\\知识星球\\生财有术\\20190904-2\\pdf\\微信（xumajie1688）生财有术[20190904].pdf')