# coding:utf-8
import zf_base
import pycurl
import io
import urllib
import urllib.parse
import certifi
import urllib.request
import re


class HttpCore(zf_base.Zhttp):
    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.CAINFO, certifi.where())
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)  # 跟踪链接和跳转
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 30)  # 链接超时时间30秒
        self.curl.setopt(pycurl.TIMEOUT, 90)  # 请求超时时间90秒
        self.curl.setopt(pycurl.MAXREDIRS, 5)  # 最大重定向次数5次
        self.curl.setopt(pycurl.COOKIEFILE, './cookie.txt')  # 保存COOKIE的文件
        self.curl.setopt(pycurl.COOKIEJAR, './cookie.txt')  # 读取COOKIE的文件
        self.curl.setopt(pycurl.USERAGENT, 'User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux i686;\
         rv:46.0) Gecko/20100101 Firefox/46.0')
        # self.curl.setopt(pycurl.VERBOSE, 1)
        self.curl.setopt(pycurl.AUTOREFERER, 1)

    def get(self, url=None, head=None):
        self.__check_args(url, head)
        if head is None:
            head = self.head
        buf = io.BytesIO()
        self.curl.setopt(pycurl.URL, url)
        # self.curl.setopt(pycurl.HEADER, True)
        self.curl.setopt(pycurl.HTTPHEADER, head)
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.perform()
        ret = buf.getvalue()
        buf.close()
        return ret

    def post_str(self, url=None, head=None, post_data=None):
        self.__check_args(url, head)
        if head is None:
            head = self.head
        if post_data is not None:
            assert isinstance(post_data, str)

        buf = io.BytesIO()
        self.curl.setopt(pycurl.URL, url)
        # self.curl.setopt(pycurl.HEADER, True)
        self.curl.setopt(pycurl.HTTPHEADER, head)
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.setopt(pycurl.POSTFIELDS, post_data)
        self.curl.perform()
        ret = buf.getvalue()
        buf.close()
        return ret

    def post_dict(self, url=None, head=None, post_data=None):
        self.__check_args(url, head)
        if head is None:
            head = self.head
        if post_data is not None:
            assert isinstance(post_data, dict)
        buf = io.BytesIO()
        self.curl.setopt(pycurl.URL, url)
        # self.curl.setopt(pycurl.HEADER, True)
        self.curl.setopt(pycurl.HTTPHEADER, head)
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.setopt(pycurl.POSTFIELDS, urllib.parse.urlencode(post_data))
        self.curl.perform()
        ret = buf.getvalue()
        buf.close()
        return ret

    @staticmethod
    def __check_args(url=None, head=None):
        if url is None:
            raise Exception('url为空')
        else:
            assert isinstance(url, str)
        if head is not None:
            assert isinstance(head, list)

    def proxy_get(self, url=None, head=None, proxy=None):
        self.__check_args(url, head)
        if head is None:
            head = self.head
        if proxy is not None:
            self.curl.setopt(pycurl.PROXY, proxy)
            self.curl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
        buf = io.BytesIO()
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.HTTPHEADER, head)
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.perform()
        ret = buf.getvalue()
        buf.close()
        return ret

    def proxy_post(self):
        pass

    def random_proxy(self):
        pass


def main():
    print(" 开始单元测试：\n")
    ohttp = HttpCore()
    r = ohttp.get("www.baidu.com").decode('utf-8')
    print("get函数测试通过") if (re.search(r'百度', r))else print("get函数测试通过")

if __name__ == '__main__':
    main()
