from django.db import models
# Create your models here.

#类别表
class Category(models.Model):
    tid = models.IntegerField(null = True)
    tname = models.CharField(max_length = 1024)

#作者表
class Author(models.Model):
    mid = models.IntegerField(null = True)
    name = models.CharField(max_length = 1024)

#标签表
class Tag(models.Model):
    name = models.CharField(max_length = 1024)

#视频信息表
class Video(models.Model):
    title = models.CharField(max_length = 3452, verbose_name = '标题')
    aid = models.IntegerField()
    view = models.IntegerField(null = True, verbose_name = '播放量')
    danmaku = models.IntegerField(null = True, verbose_name = '弹幕数')
    favourit = models.IntegerField(null = True)
    coin = models.IntegerField(null = True, verbose_name = '硬币')
    like = models.IntegerField(null = True, verbose_name = '点赞')

    author = models.ForeignKey(to = 'Author', on_delete = models.CASCADE)
    tag = models.ManyToManyField(to = 'Tag', on_delete = models.CASCADE)
