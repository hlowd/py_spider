# coding:utf-8
import requests
from pyquery import PyQuery as pq

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}


def get_http_proxy():
    handler('http_proxy.txt','wt',20)


def get_https_proxy():
    handler('https_proxy.txt','wn',20)


def get_gn_proxy():
    handler('http_gn_proxy.txt','nn',20)


def get_pt_proxy():
    handler('http_pt_proxy.txt','nt',20)


def handler(fn, para,num):
    for i in range(1, num):
        print("正在处理第{0}页数据".format(i))
        resp = requests.get(headers=header, url='http://www.xicidaili.com/{0}/{1}'.format(para, i))
        doc = pq(resp.text)
        s = doc('tr')
        with open(fn, 'wt', encoding='utf-8') as f:
            for node in s:
                speed = pq(node)('.bar').eq(0).attr('title')
                tim = pq(node)('.bar').eq(1).attr('title')
                if speed is not None and float(speed[0:-1])< 1.5 and float(tim[0:-1]) < 1.5:
                    f.writelines("http://"+pq(node)('td').eq(1).text() + ':' + pq(node)('td').eq(2).text()+"\n")
    print('{0}生成完毕!'.format(fn))


def main():
    get_http_proxy()
    get_https_proxy()
    get_gn_proxy()
    get_pt_proxy()

if __name__ == '__main__':
    main()
