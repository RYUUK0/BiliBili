from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

#在已经注册的APP中的类，django会自动执行ready方法
class MyadminConfig(AppConfig):
    name = 'myadmin'

    def ready(self):
        #自动扫描所有的myadmin文件,并执行
        autodiscover_modules('myadmin')