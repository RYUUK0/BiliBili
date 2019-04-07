"""bili_view URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from logres import views
from myadmin.service import myadmin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    re_path('^$', views.index),
    #登录
    re_path('^login/$', views.login),
    #注册
    re_path(r'^register/$', views.register),
    #注销函数
    re_path(r'^logoff/$', views.logoff),
    #设置
    re_path(r'settings/$', views.settings),


    re_path('myadmin/', myadmin.site.urls),

    #处理极验滑动验证码的视图函数
    re_path(r'^pc-geetest/register', views.get_ge etest),
    #media相关的路由设置
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT})
]
