# coding:utf-8

import sqlite3
import os
'''SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说
没有独立的维护进程，所有的维护都来自于程序本身。
在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
数据库文件，而是直接打开该数据库文件。
连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
执行完任何操作后，都不需要提交事务的(commit)

创建在硬盘上面： conn = sqlite3.connect('test.db')
创建在内存上面： conn = sqlite3.connect('"memory:')

下面我们一硬盘上面创建数据库文件为例来具体说明：
conn = sqlite3.connect('test.db')
其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

cu = conn.cursor()
这样我们就创建了一个游标对象：cu
在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动

'''

class db:
    def __init__(self,file=None,debug=False):
        self.debug = debug
        self.db = file

    def __get_conn(self,path=None):
        try:
            if path is None:
                print('生成内存数据库:[:memory:]')
                return sqlite3.connect(':memory:')
            else:
                print('硬盘数据库:[{0}]'.format(path))
                return sqlite3.connect(path)
        except Exception as e:
            print("打开数据库出错！")
            raise e

    def do_sql(self,sql=None,data=None):
        conn = self.__get_conn(self.db)
        if conn is None:
            raise Exception("链接对象为空")
        try:
            if data is not None:
                conn.execute(sql,data)
                if self.debug:
                    print('执行sql:[{0},参数:{1}]'.format(sql, data))
            else:
                conn.execute(sql)
                if self.debug:
                    print('执行sql:[{0}]'.format(sql))
            conn.commit()
        except Exception as e:
            print("({0},{1})执行失败，请检查原因！".format(sql,data))
            raise e
        finally:
            conn.close()


    def do_query(self, sql=None,data=None):
        conn = self.__get_conn(self.db)
        if conn is None:
            raise Exception("链接对象为空")
        try:
            if data is not None:
                cur = conn.execute(sql,data)
                if self.debug:
                    print('执行sql:[{0},参数:{1}]'.format(sql, data))
            else:
                cur = conn.execute(sql)
                if self.debug:
                    print('执行sql:[{0}]'.format(sql))
            conn.commit()
            return cur.fetchall()
        except Exception as e:
            print("{0}执行失败，请检查原因！".format(sql))
            raise e
        finally:
            cur.close()
            conn.close()

# ---------------START TEST---------------------
    def drop_table(self,table=None):
        if table is not None:
            sql = 'DROP TABLE IF EXISTS ' + table
            self.do_sql(sql)
            print("表删除成功")


    def create_table_test(self):
        self.do_sql(self.mk_table_sql())
        print("表创建成功")


    def mk_table_sql(self):
        sql = '''CREATE TABLE student (
        id int NOT NULL,
        name varchar(20) NOT NULL,
        gender varchar(4) DEFAULT NULL,
        age int DEFAULT NULL,
        address varchar(200) DEFAULT NULL,
        phone varchar(20) DEFAULT NULL,PRIMARY KEY (id))'''
        return sql


    def insert_test(self):
        if self.debug:
            print('插入数据测试...')
        insert_sql = '''INSERT INTO student values (?, ?, ?, ?, ?, ?)'''
        data = [(1, 'Hongten', '男', 20, '广东省广州市', '13423****62'),
                (2, 'Tom', '男', 22, '美国旧金山', '15423****63'),
                (3, 'Jake', '女', 18, '广东省广州市', '18823****87'),
                (4, 'Cate', '女', 21, '广东省广州市', '14323****32')]
        for i in data:
            self.do_sql(insert_sql,i)
        print("数据插入成功！")

    def fetch_test(self):
        if self.debug:
            print('读取数据测试...')
        fetch_sql = 'SELECT * FROM student WHERE ID = ? '
        data="1"
        result = self.do_query(fetch_sql,data)
        print(result)
        print("读取测试成功！")

    def update_test(self):
        if self.debug:
            print('更新数据测试...')
        update_sql = 'UPDATE student SET name = ? WHERE ID = ? '
        data = [('HongtenAA', 1),
                ('HongtenBB', 2),
                ('HongtenCC', 3),
                ('HongtenDD', 4)]
        for i in data:
            self.do_sql(update_sql, i)
        print("数据更新成功！")

    def delete_test(self):
        if self.debug:
            print('删除数据...')
        delete_sql = 'DELETE FROM student WHERE NAME = ? AND ID = ? '
        data = [('HongtenAA', 1),
                ('HongtenCC', 3)]
        for i in data:
            self.do_sql(delete_sql, i)


def main():
    d= db("test.db",True)
    d.create_table_test()
    d.insert_test()
    d.fetch_test()
    d.update_test()
    d.delete_test()
    d.drop_table("student")

if __name__ == '__main__':
    main()