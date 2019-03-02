


# str = '#FGO##FATE##命运冠位指定#'
# # target = str.split('#')
# # target = [i for i in target if i]
# # print(target)
####################################
#实例化时会执行test函数
# def test():
#     print('执行test函数')
#     return 'hahah'
#
# class AAA:
#     def __init__(self):
#         self.xx = test()
##############################################
# a = 'my %s is %s'
# b = a % 'sss'
######################################
#finally中语句一定会执行，即使上文中有return
# def test():
#     try:
#         a = 1
#         b = 2
#         print(a + b)
#         return True
#     except TypeError:
#         return False
#
#     finally:
#         print('函数完成')

# from gevent.pool import Pool
# from time import sleep
# pool = Pool(10)
# def func(i):
#     print('this is %s'% i)
# for i in range(1000):
#     pool.spawn(func, i)
#     sleep(1)
def yang():
    t = [1]
    n = 1
    yield t
    t = [1, 1]
    n += 1
    yield t
    while True:
        old_list = t
        new_list = []
        for i in range(n - 1):
            new_list.append(old_list[i] + old_list[i + 1])
        t = [1] + new_list + [1]
        n += 1
        yield t
n = 0
for i in yang():
    print(i)
    n += 1
    if n == 10:
        break






if __name__ == '__main__':
    pass

