# coding:utf-8

"""
首先，这个图片是3帧的gif,也就是说，
有3副图，这其实是故弄玄虚。
其次，任何一个两位数xy-(x+y)的结果，
都是9的倍数，
也就是:9,18,27,36,45,54,63,72,81,
只要保证这几个数字对应于下面的符号，
就可以了，其他的，都是增加神秘感
"""


def main():
    li=[]
    for i in range(100):
        s=str(i)
        if len(s) ==1:
            tmp ="{0}-({1}+{2}）={3}".format(s,0,s,0)
            n=0
        else:
            tmp = "{0}-({1}+{2})={3}".format(s, s[0], s[1], int(s) - (int(s[0]) + int(s[1])))
            n=int(s) - (int(s[0]) + int(s[1]))
        print(tmp)
        li.append(n)
    m={}.fromkeys(li).keys()
    print(m)


if __name__ =="__main__":
    main()