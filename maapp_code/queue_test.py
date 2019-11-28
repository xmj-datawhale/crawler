from queue import Queue
import time
def format_time():
    return "%s-%s-%s %s:%s:%s" % (
        time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour,
        time.localtime().tm_min, time.localtime().tm_sec)



# # 最多接收3个数据
# q = Queue()
#
# # put 向队列中添加数据
# q.put(1)
# q.put(2)
# q.put(3)
# while not q.empty():
#     print(q.get())
# # 获取当前队列长度
# print(q.qsize())
#
# # 取出最前面的一个数据 1 , 还剩两个
# print(q.get())
# print(q.qsize())
# # 再加入数据
# q.put(4)
#
# #超过三个了.如果没有timeout参数会处于阻塞状态,卡在那边.若设置2秒,2秒后会raise 一个 FULL的报错
# q.put(5, timeout=2)
#
# # 当然,也可以直接给个 block=False,强制设置为不阻塞(默认为会阻塞的)，一旦超出队列长度，立即抛出异常
# q.put(6, block=False)

# 同样的,当取值(get)的次数大于队列的长度的时候就会产生阻塞，设置超时时间意为最多等待x秒，队列中再没有数据，就抛出异常.
#   也可以使用block参数,跟上面一样



def exportAll5():

    for i in range(10):
        for j in range(10):
            for k in range(10):
                for n in range(10):
                    for m in range(10):
                        q.put('%s%s%s%s%s=0.1'%(str(m),str(i),str(j),str(k),str(n)))

def exportAll4():
    l=[]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for n in range(10):
                    l.append('X%s%s%s%s' % (str(i), str(j), str(k), str(n)))
    print(format_time())
    with open('D:/41_all.txt', mode='a+') as f:
        f.write(','.join(l))
    # with open('D:/004_all.txt',mode='a+') as f:
    #     f.write(','.join(l))
def exportAll():
    l=[]
    print(format_time())
    for i in range(10):
            l.append('XXXX%s=1'%(str(i)))
    print(format_time())
    for i in range(10):
        for j in range(10):
            l.append('X%sXX%s=1'%(str(i),str(j)))
    print(format_time())
    for i in range(10):
        for j in range(10):
            for k in range(10):
                    l.append('X%sX%s%s=1'%(str(i),str(j),str(k)))
    print(format_time())
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for n in range(10):
                    l.append('X%s%s%s%s=0.1'%(str(i),str(j),str(k),str(n)))
    print(format_time())
    with open('D:/all.txt',mode='a+') as f:
        f.write(','.join(l))
    print(format_time())
if __name__ == '__main__':
    # exportAll()
    exportAll4()