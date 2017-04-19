# coding utf-8
"""

"""
import multiprocessing
import time

class t_pool:
    def __init__(self):
        self.lst = [1, 2, 3, 4, 5]
        self.lst01=[(1,2,3),(2,2,3),(3,2,3),(4,2,3),(5,2,3),(6,2,3)]
        self.p = multiprocessing.Pool(processes=2,initializer=self.initlizer,initargs=(),maxtasksperchild=10)

    def initlizer(self):
        print(multiprocessing.current_process().name)

    @staticmethod
    def calc(n):
        """此方法必须是静态方法"""
        return n*n

    @staticmethod
    def calc01(n,m,p):
        """此方法必须是静态方法"""
        return n * m+p

    @staticmethod
    def cb(r):
        print("我是回调。。。")
        print(r)

    def test_map(self):
        r=self.p.map(t_pool.calc,(self.lst) )
        print(r)

    def test_apply(self):
        r = self.p.apply(t_pool.calc,(self.lst))
        print(r)

    def test_imap(self):
        r = self.p.imap(t_pool.calc,(self.lst))
        print(r)
        for i in r:
            print(i)

    def test_map_async(self):
        """使用回调来获得返回值"""
        r=self.p.map_async(t_pool.calc,(self.lst),callback=t_pool.cb )
        print("等待...")
        time.sleep(5)
        #print(r)

    def test_apply_async(self):
        """通过状态判断得到返回值"""
        r=self.p.apply_async(t_pool.calc,(2,))
        print("等待...")
        while True:
            if r.ready():
                print(r.get())
                break
            time.sleep(0.05)

    def test_starmap_async(self):
        """用列表传递多参数！！！，使用状态判断来得到结果"""
        r = self.p.starmap_async(t_pool.calc01,self.lst01)
        print(r)
        r.wait()
        if r.ready():
            print(r.get())

if __name__ == "__main__":
     m = t_pool()
     # m.test_map()
     # m.test_map_async()
     # m.test_apply()
     # m.test_apply_async()
     # m.test_imap()
     m.test_starmap_async()

