# coding:utf-8
# name:花瓣网单页爬虫
# description:从单独一页爬取画板图片

import urllib.request
import re
import zf_urllib as zflib
import zf_down
import json
import random
import time


class huaban_one_page:
    def __init__(self, url):
        self.json_header = ['Host: huaban.com',
                            'Connection: keep-alive',
                            'Accept: application/json',
                            'X-Requested-With: XMLHttpRequest',
                            'X-Request: JSON',
                            'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', \
                            'Referer: ' + url,
                            'Accept-Encoding:deflate, sdch',
                            # 这里要去掉zip
                            'Accept-Language: zh-CN,zh;q=0.8]']
        self.start_page = url
        self.oHttp = zflib.HttpCore()
        self.img_pool = set()
        self.ajax_end = 0
        self.start_dic = self.__get_start_dic()
        self.first_ajax_url = self.__get_first_ajax_url(self.start_dic)
        for i in self.start_dic['pin']['board']['pins']:
            r = i['file']['key']
            print(r)
            self.img_pool.add(r)

    def __get_start_dic(self):
        html = self.oHttp.get(self.start_page)
        app_page_tmp = re.findall(r'app\["page"\] = (.*)}}}', html.decode('utf-8'))
        app_page_json = app_page_tmp[0] + '}}}'
        dic = json.loads(app_page_json)
        return dic

    def __get_first_ajax_url(self, tmp):
        '''返回第一次ajax请求的地址'''
        self.board_id = tmp['pin']['board_id']
        self.rndstr = self.rnd8(8)
        start_max_pin = tmp['pin']['board']['pins'][19]['pin_id']
        url = r'http://huaban.com/boards/{b_id}/?{rstr}&max={pin}&limit=20&wfl=1'.format(b_id=self.board_id,
                                                                                         rstr=self.rndstr,
                                                                                         pin=start_max_pin)
        return url

    def __general_ajax_url(self, tmp):
        '''生成ajax请求的地址'''
        url = r'http://huaban.com/boards/{b_id}/?{rstr}&max={pin}&limit=20&wfl=1'.format(b_id=self.board_id,
                                                                                         rstr=self.rnd8(8),
                                                                                         pin=self.__get_max_pin(tmp))
        return url

    def __get_max_pin(self, dic):
        return dic[19]['pin_id']

    def __start_ajax(self):
        """开始第一次ajax请求"""
        result = self.oHttp.get(self.first_ajax_url, head=self.json_header).decode('utf-8')
        dic = json.loads(result)
        self.tmp = dic['board']['pins']
        for i in self.tmp:
            r = i['file']['key']
            print(r)
            self.img_pool.add(r)
        if len(self.tmp) < 20: self.ajax_end = 1
        while self.ajax_end < 1:
            time.sleep(1)
            result = self.oHttp.get(self.__general_ajax_url(self.tmp), head=self.json_header).decode('utf-8')
            self.tmp = json.loads(result)['board']['pins']
            for i in self.tmp:
                r = i['file']['key']
                print(r)
                self.img_pool.add(r)
            if len(self.tmp) < 20: self.ajax_end = 1
        print('地址采集完毕，开始下载')

    def __get_ajax_dic(self, url):
        result = self.oHttp.get(url)
        dic = json.loads(result)
        tmp = dic['board']['pins']
        return tmp

    def start(self):
        self.__start_ajax()
        for i in self.img_pool:
            baseurl = 'http://img.hb.aicdn.com/'
            zf_down.DL.down_s(baseurl + i, 'c:\\123\\' + i + '.jpg')

    def rnd8(self, num):
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        r = ''
        for i in range(num):
            r = r + alpha[random.randint(1, 25)]
        return r


def main():
    h = huaban_one_page('http://huaban.com/pins/1033768218/')
    h.start()


if __name__ == '__main__':
    main()
