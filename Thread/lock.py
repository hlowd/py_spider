# coding utf-8

import threading
import time

"""通过共享锁来控制对临界区的写入，达到同步的目的"""

r = threading.RLock()
a=0

def do_work():
        global a
        for i in range(1000):
            with r:  # 这个位置很重要
                a += 1
            print(a,threading.current_thread().getName())



def main():
    t= list()
    for i in range(10):
        t.append(threading.Thread(target=do_work).start())
        # t.join()  此处千万不能有join，否则只有第一个线程来运行
    print("----------")




if __name__ == "__main__":
    main()