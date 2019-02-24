from django.shortcuts import render, HttpResponse
from myadmin import templates

# Create your views here.


def look_test(request):
    return HttpResponse('查询')

def change_test(reqeuest, change_id):
    print(change_id)
    return HttpResponse('更改')

def add_test(request):
    return HttpResponse('增加')

def del_test(request, del_id):
    print(del_id)
    return HttpResponse('删除')