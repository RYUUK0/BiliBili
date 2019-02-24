


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

if __name__ == '__main__':
    pass

