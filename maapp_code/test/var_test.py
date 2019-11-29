class var1():
    v1=2
def f(v):
    var1.v1=v
if __name__ == '__main__':
    print(var1.v1)
    f(3)
    print(var1.v1)
    f(4)
    print(var1.v1)