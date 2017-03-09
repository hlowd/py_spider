# coding:utf-8
import zf_urllib as zflib
import pyquery
import time
import re
import sys


class LoginException(Exception):
    pass

class FailedLoginExcption(LoginException):
    def __str__(self):
        return "登录失败！"

class PassWrongException(LoginException):
    def __str__(self):
        return "用户名或者密码错误！"


class LoginPageChangedException(LoginException):
    def __str__(self):
        return "登录页面已经变更，请检查！"


class LoginOtherPlaceException(Exception):
    def __str__(self):
        return "已经在别的地方登录！"


class sxbid(object):
    def __init__(self):
        self.header = ['Host:www.sxbid.com.cn', \
                       'User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0', \
                       'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', \
                       'Accept-Language:en-US,en;q=0.5', \
                       'Connection:keep-alive']
        self.login_header = ['Referer:http://www.sxbid.com.cn/a/login?site=http://www.sxbid.com.cn/f/search/all']
        self.all_atricle_header = ['Referer:http://www.sxbid.com.cn/f/search']
        self.pick_header = ['Referer:http://www.sxbid.com.cn/f/search']

        self.login_data = {'iswebsite': "http://www.sxbid.com.cn/f/search/all?associatortype=0", \
                           'username': "www.sxzzdq.cn", \
                           'password': "456369"}
        tim = time.localtime(time.time())
        year = str(tim[0])
        month = str(tim[1]).rjust(2, '0')
        day1 = str(tim[2] - 1).rjust(2, '0')
        day2 = str(tim[2]).rjust(2, '0')
        self.post_param = 'pageNo=&pageSize=500&cId=3d6e34806adf48d5a59ad94f6f31deb5&dropdownBox=3d6e34806adf48d5a59ad94f6f31deb5&releaseType=&dropdownBox=&title=&content=&area.id=&area.name=&industryClassification=&dropdownBox=&tendereeOrg=&agencyOrg=&sYear=' + \
                          year + '&dropdownDate=' + year + '&sMouth=' + month + \
                          '&dropdownDate=' + month + '&sDay=' + day1 + '&dropdownDate=' + \
                          day1 + '&eYear=' + year + '&dropdownDate=' + year + \
                          '&eMouth=' + month + '&dropdownDate=' + month + '&eDay=' + \
                          day2 + '&dropdownDate=' + day2

        self.curl = zflib.HttpCore()

    def login(self):
        result = self.curl.post_dict('http://www.sxbid.com.cn/a/login', self.login_header, self.login_data).decode(
            'utf-8')
        if re.search(r'山西中州电气', result):
            print("登录成功！\n")
        else:
            if re.search(r'已在其他地点', result):
                raise LoginOtherPlaceException
            elif re.search(r'用户名或密码错误', result):
                raise PassWrongException
            elif re.search(r'已在其他地', result):
                raise LoginOtherPlaceException
            else:
                raise LoginException

    def logout(self):
        pass

    def get_all_article_addr(self):
        result = self.curl.post_str('http://www.sxbid.com.cn/f/search', self.all_atricle_header, self.post_param)
        ss = result.decode('utf-8')
        # 打印采集前一天包括所有文章的网页源代码
        # print(ss)
        doc = pyquery.PyQuery(ss)
        result_list = {}
        for i in doc('td a'):
            s = pyquery.PyQuery(i)
            tmp_str = s.attr('href')
            if tmp_str.find('java') == -1:
                result_list[s.attr('title')] = 'http://www.sxbid.com.cn' + tmp_str
        # 打印采集前一天包括所有文章的网页源代码
        # print(result_list)
        print("昨日发布信息总量为：", len(result_list), "条！")
        return result_list

    def get_my_article(self, url):
        res = self.curl.get(url).decode('utf-8')
        # 获取每一页源代码
        # print(res)
        if res == '':
            print('-------------------以下url获取源代码返回空串--------------------------')
            print(url)
            print("-------------------请检查网站账号情况，排查问题-----------------------")
            return 0
        doc = pyquery.PyQuery(res)
        if doc.text().find('请填写用户名') != -1:
            print("\n拉取详细信息失败，原因：需要登陆！\n")
            print("\n登陆中......!\n")
            try:
                self.login()
            except (FailedLoginExcption) as e:
                print(e)
                sys.exit()
            except (LoginOtherPlaceException) as e:
                print("网站提示已经在其他地方登录！\n")
                print("如果是本机10分钟内第一次登陆，请输入quit退出，并稍等一会！\n")
                print('如果10分钟内第二次使用本程序，请输入任意字符，并回车继续!\n')
                tmp = input("请输入命令：")
                if tmp == "quit": exit(0)
            except (Exception):
                print("-----------------------------")
                print("未知错误！")
                print("-----------------------------")
                exit(0)
        return self.match_article(doc, url)

    def match_article(self, doc, url):
        cc = doc.find('.page_main').text()
        # print(cc)
        if re.search(r'(电气)|(配电)|(KV)|(变电站)|(供电)|(尊村)|(运城)|(法律顾问)', cc, re.I) and \
                not re.search(r'(控制价)|(撤销公告)|(延期)|(变更公告)|(谈判公告)', cc):
            # print(url)
            return url
        else:
            return 0

    def pick_article(self, data=None):
        if data != None:
            assert isinstance(data, dict)
        else:
            data = {}
        pick_result = {}
        for i in data.keys():
            # 打印获取到的所有文章地址列表
            # print(i)
            if self.get_my_article(data[i]):
                print(i + "\n")
                pick_result[i] = data[i]
        print("\n----------------采集完毕----------------\n")
        print("一共采集到昨日发布匹配的信息：", len(pick_result), "条！\n")
        return pick_result

    def make_html(self, article_dict=None):
        header_str = '''
        <!DOCTYPE HTML>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title>筛选结果</title>
        <link rel="stylesheet" href="style/skin.css" type="text/css">
        </head>
        <body>
        <div class="top"></div>
        <div class="menu"><div class="menu_top"></div></div>
        <div class="container">
        <div class="a_top">
        </div>
        <div class="a_mid">
        <ul>'''

        foot_str = '''
        </ul></div>
        <div class="a_foot"></div></div>
        <div class="foothead">
        </div>
        <div class="foot"><div class="foot_logo"></div><div class="foot_logo_2"></div></div>
        </body>
        </html> '''

        print("开始生成HTML文件...\n")
        with open('./result.htm', 'w+', encoding='utf-8') as r:
            r.write(header_str)
            for i in article_dict.keys():
                r.write('<li class="line">' + "\n" + '<a href="' + article_dict[i] + \
                    '" target="_blank">' + i + '</a>' + "\n" + '</li>' + "\n")
            r.write(foot_str)
        print("ｈｔｍｌ文件生成完毕！\n")


def main():
    sx = sxbid()
    result = sx.get_all_article_addr()
    sx.make_html(sx.pick_article(result))


if __name__ == '__main__':
    main()