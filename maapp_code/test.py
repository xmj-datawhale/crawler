from bs4 import BeautifulSoup

import traceback
import math
# while True:
#     try:
#         a=1
#         if a == 1:
#             print('NO')
#             2 / 0
#         else:
#             print('OK')
#     except Exception as e:
#         traceback.print_exc()
#         a=2

# if __name__ == '__main__':
#     # soup = BeautifulSoup('', "html.parser")
#     # open()
#
#     import base64
#
#     str = '20191101'.encode(encoding='utf-8')
#
#     # 加密
#     encodestr = base64.b64encode("ag1.bbh666.com")
#     print(encodestr)  # b'aGVsbG8gd29ybGQ='
#     print(encodestr.decode())  # aGVsbG8gd29ybGQ=
#
#     # 解密
#
#     decodestr = base64.b64decode('aHR0cDovL2FnMS5hYTk3OTcuY29t')
#     print(decodestr)  # b'hello world'
#     print(decodestr.decode())  # hello world

threadDic={'thread-1':[{'termNo':'2019110201','startPage':'1','pageList':[1,3,5],'status':'0'},{'termNo':'2019110202','pageList':[1,3,5],'status':'0'}]}

# alarmDic={'20191102001':0,'20191102002':1,'20191102003':0}
# alarmDic={}
# if threadDic.get('thread-1') :
#     l=threadDic['thread-1']
#     for e in  l:
#         if e.get('status')=='0':
#
#             pageList=e.get('pageList')
#             e['status']=1
#     print(threadDic['thread-1'])
#
#
# else:
#     print('NO')

# newAlarmDic={}
# print(alarmDic)
# for (k,v) in alarmDic.items():
#     if v==0:
#         newAlarmDic[k]=v
# alarmDic=newAlarmDic
# # newAlarmDic.clear()
# print(alarmDic)
# print(len('1'.split('-')))
# print({'termNo':'2019110201'} in threadDic['thread-1'])
# d2={k:v for k,v in d1.items()  if v>90}
# for i in range(2,8):
#     print(i)

newThreadDic={}
for (k,v) in threadDic.items():
    newList=[]
    for d in v:
        if d['status']=='1':
            newList.append(d)
    newThreadDic[k]=newList
print(threadDic)
print(newThreadDic)

print('1' in '1'.split('-'))

def exportAll4():
    l=[]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for n in range(10):
                    l.append('X%s%s%s%s=0.1'%(str(i),str(j),str(k),str(n)))
    print(len(l))
    with open('D:/004_all.txt',mode='a+') as f:
        f.write(','.join(l))
def exportAll1():
    l=[]
    for i in range(10):
                    l.append('XXXX%s'%(str(i)))
    print(len(l))
    with open('D:/001_all.txt',mode='a+') as f:
        f.write(','.join(l))
def exportAll2():
    l=[]
    for i in range(10):
        for j in range(10):
                    l.append('XX%sX%s'%(str(i),str(j)))
    print(len(l))
    with open('D:/002_all.txt',mode='a+') as f:
        f.write(','.join(l))
def exportAll3():
    l=[]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                    l.append('X%s%sX%s'%(str(i),str(j),str(k)))
    print(len(l))
    with open('D:/003_all.txt',mode='a+') as f:
        f.write(','.join(l))
def base64Encode(url,d):
    import base64
    str = url.encode(encoding='utf-8')
    str1 = d.encode(encoding='utf-8')

    # 加密
    encodestr = base64.b64encode(str)
    encodestr1 = base64.b64encode(str1)
    # print(encodestr)  # b'aGVsbG8gd29ybGQ='
    print(url,(encodestr.decode()+","+encodestr1.decode()))  # aGVsbG8gd29ybGQ=
def readFileCount(path):
    with open(path,mode='r',encoding='utf-8') as f:
        count=len(f.readlines()[0].split(','))
        print(path,count)
def getXCount(s):
    count=0
    for i in range(len(s)) :
        if str.upper(s[i])!='X':
            count=+1
    return count
def exportAll4_File(fileName,reg):
    l=[]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for n in range(10):
                    l.append(reg%(str(i),str(j),str(k),str(n)))
    print(len(l))
    with open(fileName,mode='a+') as f:
        f.write(','.join(l))

v=0

def changeV1():
    # global v
    v=1
def changeV2():
    # global v
    v=2
def getNameByType(gameIndex,type) :
    if gameIndex == 3:
        if type >= 1 and type <= 10:
            tmp=(type-1)
            return str(tmp) + "XXXX"
        elif type >= 15 and type <= 24:
            tmp = (type-15)
            return "X" + (type-15) + "XXX"
        elif type >= 29 and type <= 38:
            tmp = (type - 29)
            return "XX" + str(tmp) + "XX"
        elif type >= 43 and type <= 52:
            tmp = (type - 43)
            return "XXX" + str(tmp) + "X"
        elif type >= 57 and type <= 66:
            tmp = (type - 57)
            return "XXXX" + str(tmp)
        elif type >= 108 and type <61108:
            return getDwNameByType(type)
def getDwNameByType(type):
    # str(math.floor(type / 10))
    if type < 208 :# 萬千XXX
        type -= 108        
        return str(math.floor(type / 10)) + str((str(type % 10))) + "XXX"
    elif type < 308 :# 萬X百XX
        type -= 208
        return str(math.floor(type / 10)) + "X" + (str(type % 10)) + "XX"
    elif type < 408 :# 萬XX十X
        type -= 308
        return str(math.floor(type / 10)) + "XX" + str(type % 10) + "X"
    elif type < 508 :# 萬XXX个
        type -= 408
        return str(math.floor(type / 10)) + "XXX" + (str(type % 10))
    elif type < 608 :# X千百XX
        type -= 508
        return "X" + str(math.floor(type / 10)) + str((str(type % 10))) + "XX"
    elif type < 708 :# X千X十X
        type -= 608
        return "X" + str(math.floor(type / 10)) + "X" + (str(type % 10)) + "X"
    elif type < 808 :# X千XX个
        type -= 708
        return "X" + str(math.floor(type / 10)) + "XX" + (str(type % 10))
    elif type < 908 :# XX百十X
        type -= 808
        return "XX" + str(math.floor(type / 10)) + (str(type % 10)) + "X"
    elif type < 1008 :# XX百X个
        type -= 908
        return "XX" + str(math.floor(type / 10)) + "X" + (str(type % 10))
    elif type < 1108 :# XXX十个
        type -= 1008
        return "XXX" + str(math.floor(type / 10)) + (str(type % 10))
    elif type < 2108:  # 万千百XX
        type -= 1108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "XX"
    elif type < 3108:  # 万千X十X
        type -= 2108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10) + "X"
    elif type < 4108:  # 万千XX个
        type -= 3108
        return str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "XX" + (type % 100 % 10)
    elif type < 5108:  # 万X百十X
        type -= 4108
        return str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "X"
    elif type < 6108:  # 万X百X个
        type -= 5108
        return str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10)
    elif type < 7108:  # 万XX十个
        type -= 6108
        return str(math.floor(type / 100)) + "XX" + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 8108:  # X千百十X
        type -= 7108
        return "X" + str(math.floor(type / 100)) + str(math.floor(type % 100 / 10)) + (type % 100 % 10) + "X"
    elif type < 9108:  # X千百X个
        type -= 8108
        return "X" + str(str(math.floor(type / 100))) + str(math.floor(type % 100 / 10)) + "X" + (type % 100 % 10)
    elif type < 10108:  # X千X十个
        type -= 9108
        return "X" + str(math.floor(type / 100)) + "X" + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 11108:  # XX百十个
        type -= 10108
        return "XX" + str(math.floor(type / 100)) + str(math.floor(type % 100 / 10)) + (type % 100 % 10)
    elif type < 21108:  # 万千百十X
        type -= 11108
        return str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10)) + "X"
    elif type < 31108:  # 万千百X个
        type -= 21108
        return str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + "X" + str(math.floor(type % 1000 % 100 % 10))
    elif type < 41108:  # 万千X十个
        type -= 31108
        return str(math.floor(type / 1000)) + str(math.floor(type % 1000 / 100)) + "X" + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))
    elif type < 51108:  # 万X百十个
        type -= 41108
        return str(math.floor(type / 1000)) + "X" + str(math.floor(type % 1000 / 100)) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))
    elif type < 61108:  # X千百十个
        type -= 51108
        return "X" + str(math.floor(type / 1000)) + str(str(math.floor(type % 1000 / 100))) + str(
            math.floor(type % 1000 % 100 / 10)) + str(math.floor(type % 1000 % 100 % 10))

def countFile(path):
    any4=0
    with open(path,'r',encoding='utf-8') as f:
        cxt=f.read()
        for code in cxt.split(','):
            code=code.split('=')[0]
            if  code!='':
                type_num = len([i for i in range(len(code)) if str.upper(code[i]) != 'X'])
                if type_num==4:
                    any4+=1
        print(len(cxt.split(',')),any4)

if __name__ == '__main__':
    # print(getXCount('23XXX'))
    # exportAll2()
    # exportAll1()
    # exportAll3()
    # exportAll4()
    # exportAll4_File('D:/CODE/test_4_01.txt')
    # exportAll4_File('D:/all_4_02.txt','%sX%s%s%s=0.1')
    # exportAll4_File('D:/all_4_03.txt','%s%sX%s%s=0.1')
    # exportAll4_File('D:/all_4_04.txt','%s%s%sX%s=0.1')
    # print([i for i in range(100) if i%8==0])
    # total=10
    # cut=int(total/3)
    # for i in range(cut):
    #     pageList=[]
    #     new_total=total
    #     if i+1)*cut < total:
    #         new_total=(i+1)*cut
    #     for j in range(i*cut,new_total):
    #         pageList.append(j)
    #     print(pageList)
    #
    # print([i for i in range(1,10,3)])
    #
    # for i in range(1,11,3):
    #     total=i+3
    #     if total>11:
    #         total=11+1
    #     list=[j for j in range(i,total)]
    #     print(list)
    # s1=set()
    # s1.add("a")
    # s1.add("aa")
    # s2 = set()
    # s2.add("b")
    # s2.add("bb")
    # print(s1)
    # # s1.add(s2)
    # s1=s1.union(s2)
    # print(s1)
    # for i in range(5):
    #     for j in range(5):
    #         print(i, j)
    #         if i == 3 and j == 3:
    #             break
            # else:
            #     continue
            # break
    # import os
    # deskPath=os.path.join(os.path.expanduser('~'), "Desktop")
    # with  open(os.path.join(deskPath,'test.txt'),mode='a+') as f:
    #     f.write("asdfasdf")
    # print(os.path.join(os.path.expanduser('~'), "Desktop"))
    #
    # print(os.path.exists(os.path.join(deskPath,'test.txt')))
    # print(os.path.exists(os.path.join(deskPath,'test1.txt')))
    # import re
    #
    # line = "0X0X";
    # print(len("0234".upper().split("X")))#1
    # print(len("000X".upper().split("X")))#2
    # print(len("0X0X".upper().split("X")))#3
    # print(len("0XXX".upper().split("X")))#4
    # searchObj = re.search(r'(.*) X (.*?) .*', line, re.M | re.I)
    #
    # if searchObj:
    #     print("searchObj.group() : ", searchObj.group())
    #     print("searchObj.group(1) : ", searchObj.group(1))
    #     print("searchObj.group(2) : ", searchObj.group(2))
    # else:
    #     print("Nothing found!!")
    # exportAll3()
    # exportAll1()
#     import base64
#
    # base64Encode("http://ag1.aa9797.com",'2019-12-01')
    # base64Encode("http://ag1.bbh666.com",'2019-12-01')
    # base64Encode("http://ag1.ddv888.com",'2019-12-01')
    # import os
    #
    # deskPath = os.path.join(os.path.expanduser('~'), "Desktop")
    #
    # if os.path.exists(os.path.join(deskPath, '注单.txt')):
    #     readFileCount(os.path.join(deskPath, '注单.txt'))
    # if os.path.exists(os.path.join(deskPath, '任四.txt')):
    #     readFileCount(os.path.join(deskPath, '任四.txt'))
    # if os.path.exists(os.path.join(deskPath, '任三.txt')):
    #     readFileCount(os.path.join(deskPath, '任三.txt'))
    # if os.path.exists(os.path.join(deskPath, '任二.txt')):
    #     readFileCount(os.path.join(deskPath, '任二.txt'))
    # if os.path.exists(os.path.join(deskPath, '任一.txt')):
    #     readFileCount(os.path.join(deskPath, '任一.txt'))
    # with open(r'D:/app/path.txt','r',encoding='utf-8') as f:
    #     print(f.readlines)
    # for i in range(1,20,5):
    #     print(i)
    dic={}
    dic['a']={'b':9}
    dic['d']={'b':9}
    dic['c']={'b':9}
    dic['a']=None
    for key in dic.keys():
        print(dic[key]['b'])
    # print(dic)
    # print(v)
    # changeV1()
    # print(v)
    # changeV2()
    # print(v)
    # print(sum([1,2,3]))
    #
    # print(getNameByType(3,61045))

    # countFile('D:/码码888/注单.txt')
    # countFile('D:/码码888/任四.txt')

    # code='4X399'
    # type_num = len([i for i in range(len(code)) if str.upper(code[i]) != 'X'])
    # print(type_num)
    # with open(r'D:/app/path.txt','r',encoding='utf-8') as f:
    #     print(f.readlines)

