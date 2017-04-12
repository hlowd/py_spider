# coding:utf-8
import sys
import re
sys.path.append('..')
"""
添加上面两句是要 子包 里面的模快
可以调用 父包 里面的模块的函数
"""
import requests
from PIL import Image

class bbs_125_la:

    def __init__(self):
        """
        自定义头部，覆盖掉自带的requests 头
        """
        self.header = {
            'Host': 'bbs.125.la',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,'
                               'en-US;q=0.5,en;q=0.3',
            'Referer': "http://bbs.125.la/home.php?"
                       "mod=spacecp&ac=invite",
            'DNT': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.ss = requests.Session()
        self.recp = re.compile(r'src="(misc.*?)" class')
        # 匹配验证码路径的正则
        self.ss.get("http://bbs.125.la/member.php?mod=logging"
               "&action=login"
               "&infloat=yes"
               "&handlekey=login"
               "&inajax=1"
               "&ajaxtarget=fwin_content_login")
        self.m="cSA"+ self.ss.cookies['lDlk_ecc9_sid']
        # 申请正则的 hashid ，必须ajax请求登录框，获得此id


    def get_code_pics(self,num=None):
        if num is None:num = 35
        # 此网站有访问数量限制，最多刷50次，
        # 就会要求输入验证码，这里不做讨论
        # 或取35张，足够
        for i in range(num):
            r=self.ss.get("http://bbs.125.la/misc.php?mod=seccode"
                          "&action=update"
                          "&idhash="+ self.m +
                          "&0.28765371403155193&modid=undefined").text
            # 0.28765371403155193 是js代码 math.random 生成的随机数，
            # 固定也可以
            p=self.recp.findall(r)
            # 构造验证码获取url
            r6=self.ss.get("http://bbs.125.la/"+p[0],headers = self.header)
            with open ("d:\\apcode\\"+str(i)+".png",'wb') as f:
                print("正在获取第{0}张验证码图片...".format(i))
                f.write(r6.content)

    def clear_bg(self):
        im = Image.open("d:\\apcode\\8.png")
        im2=im.convert("L")
        # 转化成灰度图
        im3=im2.point(lambda x: x>120 and 255)
        # 小于120 的当做背景 去掉，二值化
        return im3

    def clear_line(self,im):
        s=im.load()
        for i in range(2,im.size[0]-2) :
            for j in range(2,im.size[1]-2):
                if im.getpixel((i,j))==0:
                    v = 0
                    for x in [(i-1,j-1),(i-1,j),(i-1,j+1),
                        (i, j - 1), (j, j +1),
                        (i + 1, j - 1), (i+1, j ), (i + 1, j +1 )
                              ]:

                        if im.getpixel(x)== 0:
                            v+=1
                    if v<5:im.putpixel(x,255)
        im.show()


if __name__ == "__main__":
    s=bbs_125_la()
    #s.get_code_pics()
    s.clear_line(s.clear_bg())