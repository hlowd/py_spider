# coding:utf-8
import zf_base
import urllib.request
import http.cookiejar
import urllib.parse


class HttpCore(zf_base.Zhttp):

    def __init__(self):
        self.__opener = self.__build_cookie_opener()

    def post_dict(self, url=None, head=None, data=None):
        self.__check_args(url, head)
        if head == None:
            head = self.__head
        if data != None:
            assert isinstance(data, dict)
        data_parsed = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data_parsed, headers=self.__list_to_dic(head), method='POST')
        resp = self.__opener.open(req, data_parsed)
        tmp = resp.read()
        return tmp

    def post_str(self, url=None, head=None, data=None):
        self.__check_args(url, head)
        if head == None:
            head = self.head
        if data != None:
            assert isinstance(data, str)
        data_parsed = data.encode('utf-8')
        req = urllib.request.Request(url, data_parsed, headers=self.__list_to_dic(head), method='POST')
        resp = self.__opener.open(url, data_parsed)
        tmp = resp.read()
        return tmp

    def get(self, url=None, head=None):
        self.__check_args(url, head)
        if head == None:
            head = self.head
        req = urllib.request.Request(url, headers=self.__list_to_dic(head), method='GET')
        resp = self.__opener.open(req)
        tmp = resp.read()
        return tmp

    def get_headers(self, url, data, head):
        self.__check_args(url, head)
        if head == None:
            head = self.head
        if data != None:
            assert isinstance(data, dict)
        resp = self.post_dict(url, head, data)[1]
        return resp.info()

    def __build_cookie_opener(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        return opener

    def __list_to_dic(self, header):
        h = {}
        for i in header:
            tmp = i.split(':')
            h[tmp[0]] = tmp[1]
        return h

    def __check_args(self, url=None, head=None):
        if url == None:
            raise Exception('url为空')
        else:
            assert isinstance(url, str)
        if head != None:
            assert isinstance(head, list)


def main():
    print("本模块只是一个函数库,不能直接执行!")

if __name__ == '__main__':
    main()