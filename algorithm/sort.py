# coding:utf-8

r=[230,345,1,3,6,9,4,3,0,66,44]

def bubble(lst):
    """
    冒泡算法:
    先将第一个元素与每一个元素对比，将最小值换到第一个
    然后是第二个元素，与其后面的每一个元素对比，将次小
    的放到第二...,依次类推
    """
    n = len(lst)
    for i in range(n):
        for j in range(i+1,n):
            if lst[i] > lst[j]:
                lst[i],lst[j] = lst[j],lst[i]
        print(lst)
    return lst

def insert(lst):
    """
    插入排序，冒泡排序的变种，
    他从第二个元素依次先前，把最小的元素换到在前面
    """
    n=len(lst)
    for i in range(1,n):
        j=i-1             # 取当前值的前一个索引
        while j>=0:      # 判断索引，直到为0
            # 冒泡的变种，从第二个元素向前方冒泡而已
            if lst[j]>lst[j+1]:
                lst[j+1],lst[j]=lst[j],lst[j+1]
            print(lst)
            j-=1
        print("-"*40)
    print(lst)


def test_bubble():
    print("开始测试冒泡算法")
    print(r)
    print("-"*40)
    bubble(r)
    print("-"*40)

def test_insert():
    print("开始测试插入算法")
    print(r)
    print("-"*40)
    insert(r)
    print("-"*40)

if __name__ == "__main__":
    # test_bubble()
    test_insert()