from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """
    username: 账户名
    userpass: 密码
    avator: 头像图片
    create_time: 创建用户时间
    """
    username = models.CharField(max_length = 25, null = True, unique = True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(choices = ((0, '已删除'), (1, '待激活'), (2, '正常')))
    avator = models.FileField(upload_to = "avators_pic/", default = "avators_pic/111.png", verbose_name = '头像')

    def __str__(self):
        return self.username