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