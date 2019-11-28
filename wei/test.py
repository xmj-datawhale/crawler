#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/7/17 16:01
@Author  : xumj
'''
import random
import time
# login_time=time.time()
# time.sleep(3)
# print(time.time()-login_time)
# print("%s-%s-%s %s:%s:%s"%(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday,time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec))
# print("asdf {}{}".format(random.randint(0,9),random.randint(0,9)))
# print("asdf %d%d"% (random.randint(0,9),random.randint(0,9)))
# downed_order_no_list=[]
# downed_order_no_list.append("123")
# downed_order_no_list.append("323")
# print(downed_order_no_list)
print(time.localtime().tm_hour,time.localtime().tm_hour%3==0)
print(60*"*")
import os
import numpy as np
print(os.path.exists(os.path.join('./importtxt','down.txt')))
def data2txt(term_no):

    str_txt=''
    list=[]
    for i in range(51):
        # down_code = '%d%d%d%d' % (
        # random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
        down_code = '%d%dXX' % (random.randint(0, 9), random.randint(0, 9))
        # str_txt+='12XX=1'
        list.append('%s=%d'%(down_code,1))
    # ''.join(list)''.join(list1)

    print(','.join(list))
    with open(os.path.join('./importtxt','%s.txt'%(term_no)),'w') as f:
        f.write(','.join(list))
    # np.savetxt(os.path.join('./importtxt','11.txt')
# data2txt('50598854')
# print(os.path.exists(os.path.join('./importtxt','%s.txt'%('50598867'))))
# print(os.path.abspath(os.path.join('./importtxt','%s.txt'%('50598867'))))

def calc(a,b):
    s=str(a/b)
    s.split('.')[1][0]
if __name__ == '__main__':
    deskPath = os.path.join(os.path.expanduser('~'), "Desktop")
    print(deskPath)
    calc(1,3)


