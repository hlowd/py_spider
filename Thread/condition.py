# coding utf-8

import threading
import time

"""
通过共享锁来控制对临界区的写入，达到同步的目的
"""

r = threading.RLock()
c= threading.Condition(r)
# 多个线程共享一个条件，需要传入同一把锁
li =list()
a= 0
def produce():
    """
    固定格式：先获得锁，然后判断条件，等待或者继续
    """
    s=0
    with c:
        while True:
            s+=1
            if len(li) > 20:
                c.notify()
                # 发出通知，仓库满员
                c.wait()
            li.append(s)
            print(li,threading.current_thread().getName())


def consume():
    while True:
        with c:
            if len(li) <1:
                c.notify()
                # 发出通知 消耗完毕
                # 这个notify发出的通知，
                # 不一定会唤醒生产者，也可能唤醒消费者
                # 这是不可控的的
                # 所以，一般如果精确控制的话，需要先判断条件
                c.wait()
            else:
                li.pop()
                print(li, threading.current_thread().getName())
                # time.sleep(0.5)



def main():
    t1=threading.Thread(target=produce)
    t2 = threading.Thread(target=consume)
    t3 = threading.Thread(target=consume)
    t4 = threading.Thread(target=consume)
    # 多个进程的需要有缓冲，因为notify 只能
    # 随机唤醒一个进程，他可能是生产者，也可能是消费者
    t1.start()
    t2.start()
    t3.start()
    t4.start()

if __name__ == "__main__":
    main()