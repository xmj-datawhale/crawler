def f():

    # global total
    for i in range(3):
        print(T.total)
        T.total+=1
        # print(T.total)
class T(object):
    total=0
if __name__ == '__main__':
    for i in range(3):
        f()