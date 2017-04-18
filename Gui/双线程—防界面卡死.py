# coding:utf-8
from tkinter import *
import threading
import time

class  Win:
    def __init__(self,title="zf's Win"):
        self.sp_evt = threading.Event()
        self.root = Tk()
        self.root.title(title)
        self.root.geometry('200x200+200+200')
        self.root.resizable(width=False, height=False)
        self.btn = Button(master=self.root, text ="按钮",command = self.btn_cmd)
        self.btn.pack()
        self.lb_txt = StringVar()
        self.lb_txt.set("我在这里！！！！")
        self.lb = Label(master = self.root, textvariable=self.lb_txt)
        self.lb.pack()
        self.root.mainloop()

    def do_work(self):
        """
        线程工作函数
        """
        self.sp_evt.set()
        li = []
        for i in range(100):
            time.sleep(0.05)
            print(i)
            li.append(i)
        self.sp_evt.clear()

    def btn_cmd(self):
        if self.sp_evt.isSet():
            return
        else:
            self.lb_txt.set("开启！")
            t_do = threading.Thread(target = self.do_work)
            t_monitor = threading.Thread(target =self.monitor)
            t_do.daemon = True
            t_monitor.daemon=True
            t_do.start()
            t_monitor.start()

    def monitor(self):
        while True:
            if self.sp_evt.isSet():
                self.lb_txt.set("程序正在运行中...")
                time.sleep(0.5)
            else:
                self.lb_txt.set("运行完毕")
                break

if __name__ == "__main__":
    w=Win()