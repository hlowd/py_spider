# coding:utf8

"""
牛顿家有32个台阶，你一次能上1阶，也可以上2阶，最多上3阶，请问你有几种走法走到楼顶？

解题思路：
        当台阶只有1个时：只有一种 （1）
        当台阶只有2个时：只有二种 （1,1）（2）
        当台阶只有3个时：只有四种  （1,1,1）（1，2）（2,1）（3）
        当台阶有 n 个时：...
        _______________________________________________________
        假设走法的总数 y 是台阶总数n的函数，那么 y=f(n)

        我来考虑最后一步的走法：

        如果最后一步走 1 阶，那么就会有f(n-1)种走法
        如果最后一步走 2 阶，那么就会有f(n-2)种走法
        如果最后一步走 3 阶，那么就会有f(n-3)种走法

        根据题目意思可以知道：最后一步只有 3 种走法，所以，可以得到以下方程
        f(n)=f(n-1)+f(n-2)+f（n-3）
        可以看到这是一个 3 阶的斐波那契数列，所以得到以下解题方法

"""

def fib_01(n):
    '''由于递归深度的问题，此程序将不会正常工作'''
    if n <= 0: return 0
    if n == 1: return 1
    elif n == 2 :return 2
    elif n == 3: return 4
    else:
        return fib_01(n-1)+fib_01(n-2)+fib_01(n-3)


def fib_02(n):
    assert isinstance(n,int)
    a, b ,c= 1, 2, 4
    # 由于 斐波那契数列有开始，所以指定前三个数
    while n > 3:
        a, b, c = b, c ,a + b + c
        n-=1
    return c

'''
如果要得到每一步具体的走法，怎么解决？

这是一个没有个数的求和问题
最大步数: 每次走一阶，那么步子数就是n
最小步数:  n%3 ==0 时，步子数就是 n//3
           n%3 !=0 步子数就是n//3+1

x / y 	    除法运算,结果是浮点数
x%y 	    求模运算
x**y 	    x的y次方
x // y 	    两数相除向下取整
           (5//3)=1,(-5//3)=-2
'''

def big(n =1):
    if n <=0: return None
    s=''
    for i in range(n):
        s+=str(1)
    return s

def little(n):
    i = n//3
    if i < 1:return None
    s=""
    for i in range(n//3):
        s+=str(3)
    return s

def sum_list(li):
    result = 0
    for i in li:
        result += i
    return result

def start_fib(n):
    '''从最大值遍历到最小值来确定步数，
    中间经过去除包含456789的数字，
    去除0，去重复，并把最终结果为台阶
    数目的数字 做为一个列表返回
    '''
    b=big(n)
    l=little(n)
    result = dict()
    for i in range(int(l),int(b)+1):
        si=str(i)
        if not check_str(si):continue
        if sum_list(fen_str(si)) == n:
            print(i)
            result[si]=None
    print(sorted(result.keys()))


def fen_str(strn):
    """分词函数，将 数字字符串 分解成为一个个整数"""
    i = 0
    while i < len(strn):
        yield int(strn[i:i + 1])
        i+=1

def fen_list(li):
    """将包含元组的列表，分解出一个个的元祖，并返回"""
    i = 0
    while i < len(li):
        yield li[i:i + 1]
        i+=1


def check_str(strn):
    """检查数字字符串是否是有 123这三个字符组成"""
    for i in strn:
        if i not in '123':
            return False
    return True
"""
上面这个算法是遍历算法，从最小的可能数值一直到最大的数值，
可是随着台阶数量级的增加，计算量也是每次增加一个数量级，
所以这是最笨的方法
"""


"""
-----------------
所以算法就是因式分解，
从最大的3333333,分解每一个3，
就能得到所要的步骤
-----------------
"""

"""因式分解是错误的，因为他固定了最后一位，或者其中的某一位"""


def fenjie(strn):
    """因式分解函数，将一个数字字符串分解成，一个包含元组的列表"""
    res=[]
    for i in fen_list(strn):
        if i == '3':res.append(('111','12','21','3'))
        if i == '2':res.append(('11','2'))
        if i == '1':res.append(('1'))
    return res



def ivb(v1,v2):
    """
    今天才知道这玩意叫——笛卡尔积

    笛卡尔乘积是指在数学中，两个集合X和Y的笛卡尓积（Cartesian product），又称直积，
    表示为X × Y，第一个对象是X的成员而第二个对象是Y的所有可能有序对的其中一个成员。
    假设集合A={a, b}，集合B={0, 1, 2}，
    则两个集合的笛卡尔积为{(a, 0), (a, 1), (a, 2), (b, 0), (b, 1), (b, 2)}。

    :param v1: 第一个列表
    :param v2: 第二个列表
    :return: 连个列表的的笛卡尔积存入第一个，然后返回
    """
    result=[]
    for i in v1:
        for j in v2:
            result.append(i+j)
    return result

def pailie_list(li):
    """
    迭代调用一个 包含多个元组的列表 的笛卡尔积
    """
    v1 = li.pop()
    try:
        v2 = li.pop()
    except IndexError:
        v2 = None
    while v2 != None:
        v1 = ivb(v1, v2)
        try:
            v2 = li.pop()
        except IndexError:
            v2 = None
    return v1


def tkmess(n):
    """此函数是 因式分解 算法的思路整理
    目的是从台阶数目得到一个可以分解的
    数字字符串 然后通过对这个字符串进行
    因式分解，通过求笛卡尔积来确定方法
    此方法还不成熟，还在思考中。。。
    """
    if n ==1:return '1'
    if n == 2: return '2'
    if n == 3: return '3'
    if n == 4: return '13'
    if n == 4: return '13'
    if n == 7: return '313'
    j=n%3
    tmp=(n // 3)
    if tmp == 0:return print(str(j))
    if tmp == 1:return print(str(j)+'3')
    s=''
    for i in range(tmp-1):
        s+='3'
    print(s)
    print(j)
    if j==0:
        return s+'3'
    else:
        return s+str(j)+'3'

if __name__ == "__main__":
    print(len(pailie_list(fenjie('313'))))
    start_fib(7)










