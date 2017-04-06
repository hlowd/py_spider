# coding:utf8
import unittest
from py_spider.algorithm.sort import *


class test_sort(unittest.TestCase):
    def setUp(self):
        self.lst = [2,3,1,0,0]

    def tearDown(self):
        pass

    def test_bubble(self):
        self.assertEquals(bubble(self.lst),[0,0,1,2,3])

if __name__ == "__main__":
     unittest.main()