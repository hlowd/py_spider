#  coding:utf-8

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import sqlite3
import multiprocessing.process
import f_id
import py_spider.huaban_search as huaban
import time
import threading


class Spi_HuaBan:
    def __init__(self):
        self.evt = threading.Event()
        # 定义一个信号量，用于标识工作线程是否正常启动
    def do_work(self):
        """线程工作函数"""
        self.evt.set()
        h=huaban.HuaBan("椅子")
        h.start()
        self.evt.clear()

class Win:
    def __init__(self,title="zf's Win"):
        self.root = Tk()
        self.getScreenSize()
        self.root.title(title)
        self.root.geometry(str(self.__w)+"x"+str(self.__h)+"+"+str(self.__x)+"+"+str(self.__y))
        self.root.resizable(width=False, height=False)

        self.seeFileInit()
        self.spiderInit()


        self.root.mainloop()

    def seeFileInit(self):
        self.see_file = LabelFrame(master=self.root, text="文件识别", borderwidth=5)
        self.see_file.pack(side='top', fill='x', padx=10, pady=10)
        self.btn_sf = Button(master=self.see_file, text="选择文件...",command = self.seeFileCmd)
        self.btn_sf.pack(side = 'left', padx=5, pady=5)
        self.lb_txt = StringVar()
        self.lb_sf =Label(master=self.see_file,textvariable=self.lb_txt )
        self.lb_sf.pack(side = 'left', padx=5, pady=5)

    def seeFileCmd(self):
        fn=filedialog.askopenfilename()
        id =f_id.FileType.get_file_id(fn)
        conn = sqlite3.connect("zf.sqlite3")
        sql = 'select * from {0} where id = "{1}"'.format('FileType',id)
        result = f_id.FileType.list_to_str(conn.execute(sql).fetchall())
        self.lb_txt.set(fn+" : "+result)

    def spiderInit(self):
        self.spider_frame = LabelFrame(master=self.root, text="爬虫工程", borderwidth=5)
        self.spider_frame.pack(fill='x', padx=10, pady=10)
        self.btn_huaban = Button(master=self.spider_frame, text="花瓣网",command = self.huabanCmd)
        self.btn_huaban.pack(side='left', padx=5, pady=5)
        self.lb_spider_txt = StringVar()
        self.lb_spider = Label(master=self.spider_frame, textvariable=self.lb_spider_txt)
        self.lb_spider.pack(side='left', padx=5, pady=5)
        self.huaban = Spi_HuaBan()




    def huabanCmd(self):
        if self.huaban.evt.isSet():
            return
        else:
            self.lb_spider_txt.set("开启！")
            t_do = threading.Thread(target =self.huaban.do_work)
            t_monitor = threading.Thread(target =self.huaban_monitor)
            t_do.daemon = True
            t_monitor.daemon=True
            t_do.start()
            t_monitor.start()

    def huaban_monitor(self):
        while True:
            if self.huaban.evt.isSet():
                self.lb_spider_txt.set("程序正在运行中...")
                time.sleep(0.5)
            else:
                self.lb_spider_txt.set("运行完毕")
                break



    def spider_huaban(self,args="保险丝"):
        h = huaban.HuaBan(args)
        h.start()


    def test(self):
        for i in range(10):
            time.sleep(0.05)
            self.lb_spider_txt.set((i))
            # self.lb_spider_txt.set(str(i))

    def getScreenSize(self):
        scn_w = self.root.winfo_screenwidth()
        scn_h = self.root.winfo_screenheight()
        self.__w =int(scn_w/2)
        self.__h = int(scn_h/2)
        self.__x = int(scn_w/4)
        self.__y = int(scn_h/4)


def main():
    zf =Win(title="主窗口")


if __name__ == '__main__':
    main()