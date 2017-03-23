#  coding:utf-8

from tkinter import *
from tkinter.ttk import *
from  py_spider import f_id
from tkinter import filedialog
class Win:
    def __init__(self,title="zf's Win"):
        self.root = Tk()
        self.getScreenSize()
        self.root.title(title)
        self.root.geometry(str(self.__w)+"x"+str(self.__h)+"+"+str(self.__x)+"+"+str(self.__y))
        self.root.resizable(width=False, height=False)
        self.seeFileInit()

        #self.root.set
        self.root.mainloop()
    def seeFileInit(self):
        self.see_file = LabelFrame(master=self.root, text="文件识别", borderwidth=5)
        self.see_file.pack(side='top', fill='x', padx=10, pady=10)
        self.sf_entry = Entry(master=self.see_file)
        self.sf_entry.pack(side = 'left',padx=5, pady=5)
        self.btn_sf = Button(master=self.see_file, text="选择文件...",command = self.seeFileCmd)
        self.btn_sf.pack(side = 'left', padx=5, pady=5)
        self.lb_txt = StringVar()
        self.lb_sf =Label(master=self.see_file,textvariable=self.lb_txt)
        self.lb_sf.pack(side = 'left', padx=5, pady=5)

    def seeFileCmd(self):
            fn=filedialog.askopenfilename()
            print(fn)
            if fn is not None:
                tmp = f_id.getVector(fn)
                print(tmp)
                self.lb_txt.set(str(tmp[0])+ "    "+str(tmp[1]))








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