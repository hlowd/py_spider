# coding utf-8
import threading
import time
s = threading.Semaphore(5)

def do_work():
    for i in range(s._value+1000):
        print(i)
        s.acquire()

def do_start():
    while True:
        tmp = input("请输入一个大100的数，来释放资源，增加信号量:")
        if int(tmp) >100:
            s.release()
            time.sleep(2)




def main():
    t1 =threading.Thread(target = do_work)
    t2=threading.Thread(target=do_start)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()