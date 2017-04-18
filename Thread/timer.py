# coding utf-8

import threading
import time
"""此种定时器只执行一次"""
def do_work():
    print(time.localtime())

def main():
    t= threading.Timer(2,do_work)
    t.start()
    print("----------")
    time.sleep(10)




if __name__ == "__main__":
    main()