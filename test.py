#coding:utf-8

import re
import urllib.request
import os.path

def getHtml(url):
    page = urllib.request.urlopen(str(url))
    htm = page.read().decode('utf-8')
    return htm


def getImg(html):
    reg = r'src="(http.*?\.jpg)" size='
    imgre=re.compile(reg)
    imglist=imgre.findall(html)
    os.mkdir("c:\\123")
    for imgurl in imglist:
        print("正在下载{0}".format(imgurl))
        urllib.request.urlretrieve(imgurl,"c:\\123\\{0}.jpg".format(os.path.basename(imgurl)))

html=getHtml("https://tieba.baidu.com/p/5048432758")
getImg(html)