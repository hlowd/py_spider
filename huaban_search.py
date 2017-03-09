# coding:utf-8
import urllib.request
import urllib.parse
import re
import zf_urllib as zflib
import zf_down
import json
import random
import time


class JsonHeader:
    def __init__(self, url):
        self.json_header = ['Host: huaban.com',
                            'Connection: keep-alive',
                            'Accept: application/json',
                            'X-Requested-With: XMLHttpRequest',
                            'X-Request: JSON',
                            'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                            'Referer: ' + url,
                            'Accept-Encoding:deflate, sdch',
                            # 这里要去掉zip
                            'Accept-Language: zh-CN,zh;q=0.8]']


class HuaBan:
    def __init__(self, kword):
        self.oHttp = zflib.HttpCore()
        self.kw = kword

    def start(self):
        pin_pool = self.get_pin(self.kw)
        for i in pin_pool:
            url = 'http://huaban.com/pins/{0}/'.format(i)
            img_pool = self.get_page_addr(url)
            self.down_img(img_pool)

    def get_pin(self, kword = None, mx = None):
        if mx is None:
            mx = 100
        url = 'http://huaban.com/search/?q=' + urllib.parse.quote(kword)
        html = self.oHttp.get(url)
        h = JsonHeader(url).json_header
        s1 = re.findall(r'app.page\[\"pins\"\] = (.*)}}];', html.decode('utf-8'))
        print(s1)
        s = s1[0] + '}}]'
        dic = json.loads(s)
        print(dic[0]['pin_id'])
        add = set()
        for i in dic:
            add.add(i['pin_id'])
        p = 2
        while True:
            print("正在爬取第{0}页数据...".format(p))
            html = self.oHttp.get('{u}&{rd8}&page={page}&per_page=20&wfl=1'\
                                  .format(u=url, rd8=self.rnd_str(8), page=str(p)), head=h)
            ss = json.loads(html.decode("utf-8"))
            tmp = len(ss['pins'])
            if tmp > 0:
                try:
                    for i in ss['pins']:
                        if i['pin_id'] is not None:
                            add.add(i['pin_id'])
                except Exception as e:
                    print(e, '错误发生在第{page}页！'.format(page=p))
                    print(html.decode('utf-8'))
            if tmp < 20:
                break
            # 如果返回json的pin数量小于20，则表明pin数据采集完毕
            p += 1
            if p > mx:
                break
        print('花瓣网搜索{k},总共获取有效pin{n}个！'.format(k=kword, n=len(add)))
        return add

    def get_page_addr(self, url):
        print('-'*60)
        print("开始处理：" + url)
        img_pool = set()
        html = self.oHttp.get(url)
        app_page_tmp = re.findall(r'app\["page"\] = (.*)}}}', html.decode('utf-8'))
        app_page_json = app_page_tmp[0] + '}}}'
        start_dic = json.loads(app_page_json)
        for i in start_dic['pin']['board']['pins']:
            r = i['file']['key']
            img_pool.add(r)
        # 处理单页未曾ajax请求之前得到的图片地址，加入地址池
        first_ajax_url = self.__get_first_ajax_url(start_dic)
        # 开始第一次ajax请求
        h = JsonHeader(url).json_header
        # -------------------
        print(first_ajax_url)
        print(h)
        # --------------------
        result = self.oHttp.get(first_ajax_url, head=h).decode('utf-8')
        dic = json.loads(result)
        tmp = dic['board']['pins']
        for i in tmp:
            r = i['file']['key']
            print(r)
            # 返回该页面第一次ajax加载的每一幅图片的文件名，并增添到地址池中
            img_pool.add(r)
        if len(tmp) < 20:
            return img_pool
        # 如果地址数量少于20，则说明资源已经加载完了，可以直接返回，否则进入下面的循环
        while True:
            time.sleep(1)
            result = self.oHttp.get(self.__general_ajax_url(tmp), head=h).decode('utf-8')
            tmp = json.loads(result)['board']['pins']
            for i in tmp:
                r = i['file']['key']
                print(r)
                img_pool.add(r)
            if len(tmp) < 20:
                print('-'*20 + url + '地址采集完毕，开始下载' + '-'*20)
                return img_pool

    def __get_first_ajax_url(self, tmp):
        """返回第一次ajax请求的地址"""
        self.board_id = tmp['pin']['board_id']
        num = len(tmp['pin']['board']['pins'])
        start_max_pin = tmp['pin']['board']['pins'][num-1]['pin_id']
        url = r'http://huaban.com/boards/{b_id}/?{rstr}&max={pin}&limit=20&wfl=1'.format(b_id=self.board_id, rstr=self.rnd_str(8), pin=start_max_pin)
        return url

    def __general_ajax_url(self, tmp):
        """生成ajax请求地址"""
        url = r'http://huaban.com/boards/{b_id}/?{rstr}&max={pin}&limit=20&wfl=1'.\
            format(b_id=self.board_id, rstr=self.rnd_str(8), pin=self.__get_max_pin(tmp))
        return url

    def down_img(self,i_pool):
        for i in i_pool:
            baseurl = 'http://img.hb.aicdn.com/'
            zf_down.DL.down_s(baseurl+i, 'c:\\123\\' + i + '.jpg')

    def rnd_str(self,num):
        alpha1 = 'abcdefghijklmnopqrstuvwxyz'
        alpha2 = 'abcdefghijklmnopqrstuvwxyz123456789'
        r = alpha1[random.randint(0, 25)]
        for i in range(num-1):
            r += alpha2[random.randint(0, 34)]
        return r

    def __get_max_pin(self, dic):
        num = len(dic)
        return dic[num - 1]['pin_id']


def main():
    h = HuaBan('保险丝')
    h.start()

if __name__ == '__main__':
    main()
