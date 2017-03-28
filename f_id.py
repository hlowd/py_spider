# coding:utf-8
import sys
import sqlite3
import os


class Info:
    tp = dict()
    tp["49492a00227105008037"] = "tif"     # TIFF [tif)
    tp["424d228c010000000000"] = "bmp"     # 16色位图[bmp)
    tp["424d8240090000000000"] = "bmp"     # 24位位图[bmp)
    tp["424d8e1b030000000000"] = "bmp"     # 256色位图[bmp)
    tp["41433130313500000000"] = "dwg"     # CAD [dwg)
    tp["7b5c727466315c616e73"] = "rtf"     # Rich Text Format [rtf)
    tp["38425053000100000000"] = "psd"     # Photoshop [psd)
    tp["46726f6d3a203d3f6762"] = "eml"     # Email [Outlook Express 6] [eml)
    tp["d0cf11e0a1b11ae10000"] = "doc"     # MS Excel 注意：word、msi 和 excel的文件头一样
    tp["d0cf11e0a1b11ae10000"] = "vsd"     # Visio 绘图
    tp["5374616E64617264204A"] = "mdb"     # MS Access [mdb)
    tp["252150532D41646F6265"] = "ps"      #
    tp["255044462d312e350d0a"] = "pdf"     # Adobe Acrobat [pdf)
    tp["2e524d46000000120001"] = "rmvb"    # rmvb/rm相同
    tp["464c5601050000000900"] = "flv"     # flv与f4v相同
    tp["00000020667479706d70"] = "mp4"
    tp["49443303000000002176"] = "mp3"
    tp["000001ba210001000180"] = "mpg"
    tp["3026b2758e66cf11a6d9"] = "wmv"     # wmv与asf相同
    tp["52494646e27807005741"] = "wav"     # Wave [wav)
    tp["52494646d07d60074156"] = "avi"
    tp["4d546864000000060001"] = "mid"     # MIDI [mid)
    tp["504b0304140000000800"] = "zip"
    tp["526172211a0700cf9073"] = "rar"
    tp["504b03040a0000000000"] = "jar"
    tp["4d5a9000030000000400"] = "exe"    # 可执行文件
    tp["4d616e69666573742d56"] = "mf"    # MF文件
    tp["494e5345525420494e54"] = "sql"    # xml文件
    tp["1f8b0800000000000000"] = "gz"    # gz文件
    tp["6c6f67346a2e726f6f74"] = "properties"    # bat文件
    tp["cafebabe0000002e0041"] = "class"    # bat文件
    tp["49545346030000006000"] = "chm"    # bat文件
    tp["04000000010000001300"] = "mxp"    # bat文件
    tp["504b0304140006000800"] = "docx"    # docx文件
    tp["d0cf11e0a1b11ae10000"] = "wps"    # WPS文字wps、表格et、演示dps都是一样的
    tp["6431303a637265617465"] = "torrent"


class FileType:
    def __init__(self):
        self.db = 'zf.sqlite3'
        self.tb = 'FileType'
        self.conn = self.get_conn()

    @staticmethod
    def get_dir_files(dir,li):
        try:
            for i in os.listdir(dir):
                p = os.path.join(dir, i)
                if os.path.isfile(p):
                    li.append(p)
                elif os.path.isdir(p):
                    FileType.get_dir_files(p, li)
                else:
                    continue
        except Exception as e:
            print(e)

    @staticmethod
    def get_file_id(fn):
        r = str()
        try:
            with open(fn, 'rb') as f:
                t5 = f.read(4)
                for i in range(4):
                    if 15 >= t5[i] >= 0:
                        r += '0' + hex(t5[i])[2:4]
                    else:
                        r += hex(t5[i])[2:4]
        except Exception:
            return '00000000'
        return r

    @staticmethod
    def get_file_ext(fn):
        import os
        if os.path.exists(fn) and os.path.isfile(fn):
            (dirPath, fileName) = os.path.split(fn)
            (basename, ext) = os.path.splitext(fileName.lower())
            return ext
        else:
            return 'None'

    @staticmethod
    def get_file_data(fn):
        return FileType.get_file_id(fn), FileType.get_file_ext(fn)

    @staticmethod
    def dup_remove(lst):
        """列表去重"""
        return {}.fromkeys(lst).keys()

    @staticmethod
    def wash_data(lst):
        sIdList = list()
        for i in lst:
            sIdList.append(i[0])
        didlist = FileType.dup_remove(sIdList)
        # --------取出唯一的id ,并形成列表--------
        cleanData =list()
        for i in didlist:
            ext = list()
            for j in lst:
                if j[0] == i:
                    ext.append(j[1])
            ext_dup_remove = FileType.dup_remove(ext)
            ext_str = FileType.list_to_str(ext_dup_remove)
            cleanData.append((i,ext_str))
        # --------遍历文件指纹，并把指纹相同的扩展名进行合并，形成以指纹为id的唯一记录 --------
        return cleanData


    @staticmethod
    def list_to_str(list):
        s= str()
        for i in list:
            s += str(i)
        return s

    def insert_list(self,list_data=list()):
        sql = 'insert into {0} (id,ext) values(?,?)'.format(self.tb)
        try:
            self.conn.executemany(sql,list_data)
            self.conn.commit()
        except Exception as e:
            print("批量插入数据失败，失败原因:{e}".format(e))

    def insert_one(self,set_data=set()):
        sql = 'insert into {0} (id,ext) values{1}'.format(self.tb,set_data)
        try:
            self.conn.execute(sql)
            self.conn.commit()
            print("{0}表中成功插入数据:{1}".format(self.tb,set_data))
        except Exception:
            print("{0}表中成功插入数据:{1}".format(self.tb,set_data))

    def select_all(self):
        sql = 'select * from {0}'.format(self.tb)
        try:
            cur=self.conn.execute(sql)
            return cur.fetchall()
        except Exception as e:
            print("获取表中所有数据失败，失败原因:{0}".format(e))
            return None

    def delete_all_rows(self):
        sql = "DELETE FROM {0}".format(self.tb)
        try:
            self.conn.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("清空表中所有数据失败，失败原因:{0}".format(e))

    def get_conn(self):
        conn = sqlite3.connect(self.db)
        c1 = conn.execute("""select count(*) from sqlite_master where type='table' and name='{0}'""".format(self.tb))
        if c1.fetchone()[0] == 0:
            conn.execute('''CREATE TABLE FileType
                           (id varchar(10) primary key  NOT NULL,
                            ext   varchar(500)   NOT NULL);''')
        conn.commit()
        return conn

    def feed_db(self,dirName):
        foods = list()
        new_data = list()
        FileType.get_dir_files(dirName, foods)
        print("获取新增文件列表，共有新文件{0}个！".format(len(foods)))
        print("开始获取文件特征！")
        for i in foods:
            new_data.append(FileType.get_file_data(i))
        old_data = self.select_all()
        if old_data is None:
            while True:
                tmp = input("旧数据为空，仅使用新数据?:(继续：y 退出 :n):")
                if "n" == tmp:
                    print("用户选择退出，请检查数据库状况!!!")
                    sys.exit(1)
                elif "y" == tmp:
                    old_data = []
                    break
                else:
                    continue
        new_data += old_data
        print("开始清洗数据，去重和合并新旧数据！")
        clean_data = FileType.wash_data(new_data)
        print("删除旧表所有数据！")
        self.delete_all_rows()
        print("删除旧表所有数据完毕！")
        self.insert_list(list_data=clean_data)
        print("插入生成的新数据！")
        self.conn.close()
        print("数据库数据更新完毕！")

    def select_data(self,str_data):
        sql = 'select * from {0} where id = {1}'.format(self.tb,str_data)
        try:
            cur = self.conn.execute(sql)
            return cur.fetchall()
        except Exception as e:
            print("获取表中所有数据失败，失败原因:{0}".format(e))
            return None


def main(argv):
    s = FileType()
    s.feed_db("f:")

if __name__ == '__main__':
    main(sys.argv)
