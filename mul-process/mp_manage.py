# coding:utf-8

import multiprocessing


def main():
    m= multiprocessing.Manager()
    l= m.list((1,2,3,4,5,6))
    print(l)
    print(repr(l))


if __name__ == "__main__":
    main()