import urllib.request

class DL:
    @staticmethod
    def down_s(url, file_name):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:50.0) Gecko/20100101 Firefox/50.0'}
        req = urllib.request.Request(url=url, headers=header)
        resp = urllib.request.urlopen(req)
        file_size = int(resp.getheader("Content-Length"))
        print('-' * 100)
        print('开始下载文件:', url, '\n\n文件大小为:', file_size / 1024, 'KB\n')
        with open(file_name, 'wb') as f:
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = resp.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                print('已经下载：', file_size_dl / file_size * 100, '%\n')
        print('已经另存为：', file_name)
        print('-' * 50)
