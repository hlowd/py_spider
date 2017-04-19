# coding utf-8
"""
多生产者-多消费者模型
先进先出的队列
已经自己实现同步
"""

import threading
import queue

q= queue.Queue(5)

def produce():
    for i in range(50000):
        q.put(i)


def consume():
    while True:
        n=q.get()
        print(n, threading.current_thread().getName())

def main():
    t10= threading.Thread(target=produce)
    #t11 = threading.Thread(target=produce)
    #t12 = threading.Thread(target=produce)
    t20 = threading.Thread(target=consume)
    t21 = threading.Thread(target=consume)
    t22 = threading.Thread(target=consume)
    t10.start()
    t20.start()
    t21.start()
    t22.start()



if __name__ == "__main__":
    main()