# coding:utf-8
import hashlib
import multiprocessing.pool
from py_spider.f_id import FileType
import time
def file_md5(file):

    """计算文件的MD5值"""

    md5_value = hashlib.md5()
    with open(file,"rb") as f:
        while True:
            data = f.read(2048)#每次只读取2048字节
            if data == b'':
                break
            md5_value.update(data)# 更新MD5值
        print(multiprocessing.current_process())
        return file,md5_value.hexdigest()


def init(arg):
    print(arg)

def cb(ar):
    print(ar)



def map_md5_async():
    "异步多进程获取文件夹下文件的MD5"
    li=[]
    FileType.get_dir_files('.',li)
    p= multiprocessing.Pool(initializer=init,initargs=("pool is start!!!",),maxtasksperchild=10)
    p.map_async(file_md5,li,callback=cb)
    p.close()
    print("----------")
    print(p.get())

def t1(n):
    for i in range(n):
        time.sleep(0.5)
        print(i)
    return n+1

def file_ma5_apply_async():
    li = []
    FileType.get_dir_files('.', li)
    p = multiprocessing.Pool(initializer=init, initargs=("pool is start!!!",), maxtasksperchild=5)
    p.apply_async(t1,args=(5,),callback=cb)
    p.close()
    print("----------")
    p.join()



def map_md5():
    "多进程获取文件夹下文件的MD5"
    li=[]
    FileType.get_dir_files('.',li)
    p= multiprocessing.Pool()
    s=p.map(file_md5,li)
    p.close()
    print("------------------")
    p.join()
    print(s)


def test():
    # map_md5_async()
    # map_md5()
    file_ma5_apply_async()



if __name__ == "__main__":
    test()