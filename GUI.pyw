#  coding:utf-8

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import sqlite3
import multiprocessing.process
import f_id
import huaban_search as huaban
import time
class Win:
    def __init__(self,title="zf's Win"):
        self.root = Tk()
        self.getScreenSize()
        self.root.title(title)
        self.root.geometry(str(self.__w)+"x"+str(self.__h)+"+"+str(self.__x)+"+"+str(self.__y))
        self.root.resizable(width=False, height=False)

        self.seeFileInit()
        self.spiderInit()

        self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        #self.root.set
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
        self.lb_sf.pack(side='left', padx=5, pady=5)


    def huabanCmd(self):
        self.btn_huaban.configure(state='disable')
        print(multiprocessing.cpu_count())
        self.pool.apply_async(func=self.test(),callback=self.f_call())
        self.pool.close()
        print("111111111111111")
        self.lb_spider_txt.set("正在处理")
        print(self.lb_spider_txt.get())


    def spider_huaban(self,args="保险丝"):
        h = huaban.HuaBan(args)
        h.start()


    def test(self):
        for i in range(50):
            time.sleep(0.5)
            print(i)
            # self.lb_spider_txt.set(str(i))

    def f_call(self):
        print("jieshu")
        self.btn_huaban.configure(state='normal')


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