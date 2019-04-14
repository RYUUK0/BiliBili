from django.urls import path, re_path
from interview import views

urlpatterns = [
    re_path(r'^$', views.get_interview_index),
    re_path(r'add/$', views.Add.as_view()),
    re_path(r'date/$', views.Date.as_view()),
    re_path(r'chat/$', views.Chat.as_view()),

]