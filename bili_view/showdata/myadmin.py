from django.contrib import admin
from myadmin.service import myadmin
from django.utils.safestring import mark_safe
from showdata import models
from django.urls import reverse


class VideoConfig(myadmin.ModelMyadmin):
    display = ['title', 'views', 'coin', 'danmaku']
    filter_list = ['author', 'tag']
    actions = []
    search_fields = ['title', 'aid']





myadmin.site.register(models.Author)
myadmin.site.register(models.Category)
myadmin.site.register(models.Tag)
myadmin.site.register(models.Video, VideoConfig)
