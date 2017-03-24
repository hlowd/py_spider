# coding:utf-8
import sys
import sqlite3
import os


class Info:
    tp = dict()
    tp["jpg"] = "JPEG [jpg)"
    tp["png"] = "PNG [png)"
    tp["gif"] = "gif"
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


def genFileList(dir,li):
    for i in os.listdir(dir):
        p = os.path.join(dir, i)
        if os.path.isfile(p):
            li.append(p)
        elif os.path.isdir(p):
            genFileList(p,li)
        else:
            continue




def getFileID(fn):
    r = str()
    size = os.path.getsize(fn)
    try:
        with open(fn, 'rb') as f:
            t5 = f.read(4)
            for i in range(4):
                if 15 >= t5[i] >= 0:
                    r += '0'+ hex(t5[i])[2:4]
                else:
                    r += hex(t5[i])[2:4]
    except Exception:
        return '00000000'
    return r


def getFileExtName(fn):
    import os
    if os.path.exists(fn) and os.path.isfile(fn):
        (filepath, tempfilename) = os.path.split(fn)
        (shotname, extension) = os.path.splitext(tempfilename)
        return extension
    else:
        return 'None'


def getFileData(fn):
    return getFileID(fn),getFileExtName(fn)

def insert(listdata=list(),tb=None):
    if tb is None:raise Exception("tb 参数不能为空")
    conn = getConn()
    sql = 'insert into {0} (vec,extname) values(?,?)'.format(tb)
    try:
        conn.executemany(sql,listdata)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def getConn(tb1='FileTypeN',tb2='FileType'):
    conn = sqlite3.connect("zf.db")
    c1 = conn.execute("""select count(*) from sqlite_master where type='table' and name='{0}'""".format(tb1))
    c2 = conn.execute("""select count(*) from sqlite_master where type='table' and name='{0}'""".format(tb2))
    if c1.fetchone()[0] == 0:
        conn.execute('''CREATE TABLE FileTypeN
                       (vec varchar(5)  NOT NULL,
                        extname   varchar(5)   NOT NULL);''')
    if c2.fetchone()[0] == 0:
        conn.execute('''CREATE TABLE FileType
                       (vec varchar(5) PRIMARY KEY  NOT NULL,
                        extname   varchar(5)   NOT NULL);''')
    conn.commit()
    c1.close()
    c2.close()
    return conn


def washingDB(tb1='FileTypeN',tb2='FileType'):
    conn = getConn()
    c1 =conn.execute("select * from {}".format(tb1))
    tmp =c1.fetchall()
    print(tmp)


def handler(fn):
    r = str()
    with open(fn, 'rb') as f:
        t10 = f.read(10)
        for i in range(10):
            if 9 >= t10[i] >= 0:
                r += '0'+ hex(t10[i])[2:4]
            else:
                r += hex(t10[i])[2:4]
    print('-' * 40)
    if r in Info.tp.keys():
        print('-'*40)
        print("{0}的文件类型是:{1}".format(fn, Info.tp[r]))
        print('-'*40)


def dup_remove(list):
    """列表去重"""
    return {}.fromkeys(list).keys()


def main(argv):
    li = list()
    r=[]
    genFileList("d:\\tool",li)
    for i in li:
        r.append(getFileData(i))
    print(r)
    washingDB()


if __name__ == '__main__':
    main(sys.argv)
