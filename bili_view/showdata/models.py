from django.db import models
# Create your models here.

#类别表
class Category(models.Model):
    tid = models.IntegerField(primary_key = True)
    tname = models.CharField(max_length = 1024)

    def __str__(self):
        return self.tname

#作者表
class Author(models.Model):
    mid = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 1024)

    def __str__(self):
        return self.name

#标签表
class Tag(models.Model):
    name = models.CharField(max_length = 1024)

    def __str__(self):
        return self.name

#视频信息表
class Video(models.Model):
    title = models.CharField(max_length = 3452, verbose_name = '标题')
    aid = models.IntegerField(unique = True)
    views = models.IntegerField(null = True, verbose_name = '播放量')
    danmaku = models.IntegerField(null = True, verbose_name = '弹幕数')
    favourit = models.IntegerField(null = True)
    coin = models.IntegerField(null = True, verbose_name = '硬币')
    likes = models.IntegerField(null = True, verbose_name = '点赞')


    author = models.ForeignKey(to = 'Author', on_delete = models.CASCADE, null = True)
    category = models.ForeignKey(to = 'Category', on_delete = models.CASCADE, null = True)
    tag = models.ManyToManyField(to = 'Tag')

    def __str__(self):
        return self.title
