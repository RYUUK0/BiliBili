from django.contrib import admin
from myadmin.service import myadmin
from django.utils.safestring import mark_safe
from showdata import models
from django.urls import reverse

myadmin.site.register(models.Author)
myadmin.site.register(models.Category)
myadmin.site.register(models.Tag)
myadmin.site.register(models.Video)
