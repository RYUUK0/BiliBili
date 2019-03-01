from django.contrib import admin
from myadmin.service import myadmin
from django.utils.safestring import mark_safe
from showdata import models
from django.urls import reverse


class VideoConfig(myadmin.ModelMyadmin):

    def jump_link(self, obj, is_head = False):
        if is_head:
            return '操作'
        _url = 'https://www.bilibili.com/%s'%('av' + str(obj.aid))
        res = "<a href='%s'target='_blank'>%s</a>"%(_url, '跳转')
        return mark_safe(res)

    display = ['title', 'views', 'coin', 'danmaku', jump_link]
    filter_list = ['author', 'tag']
    actions = []
    search_fields = ['title', 'aid']
    sort_list = ['views', 'coin', 'danmaku']







myadmin.site.register(models.Author)
myadmin.site.register(models.Category)
myadmin.site.register(models.Tag)
myadmin.site.register(models.Video, VideoConfig)
