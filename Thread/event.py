# coding utf-8

import threading

ev = threading.Event()

def do_work():
    """
    t1 线程函数
    程序一开始就等待t2 的信号
    :return:
    """
    ev.wait()
    if ev.isSet():
        for i in range(100):
            print(i)
    ev.clear()

def do_start():
    """
    t2的线程函数，依靠用户的输入来
    决定是否设置信号

    """
    while True:
        s=input("输入一个数字")
        if int(s)>100:
            ev.set()
            break


def main():
    t1=threading.Thread(target = do_work)
    t2 = threading.Thread(target=do_start)
    t1.start()
    t2.start()
    # 同时启动两个进程，但是 t1 要等待 t2 的消息

if __name__ == "__main__":
    main()