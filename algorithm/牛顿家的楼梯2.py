# coding:utf-8
import timeit

def fib_count(n):
    a, b, c = 1, 2, 4
    if n == 1: return a
    if n == 2: return b
    if n == 3: return c
    while n > 3:
        a,b,c = b,c,a+b+c
        n -= 1
    return c

def fib_p(n):
    o=[""]
    m=n
    while n>0:
        o=expand_list(o,m)
        n-=1
        for i in o:
            if count_str(i) == m: print(i)

def expand_list(li,n):
    r=[]
    for i in li:
        if count_str(i)>n:continue
        r.append(i+"1")
        r.append(i+"2")
        r.append(i+"3")
    return r


def main(n):
    print("{0}级台阶共有{1}种走法:".format(n, fib_count(n)))
    fib_p(n)

def count_str(s):
    c=0
    for i in s:
        c+=int(i)
    return(c)

if __name__ == "__main__":
    main(5)