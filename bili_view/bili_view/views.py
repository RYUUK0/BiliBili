from myadmin.service import myadmin
from django.shortcuts import HttpResponse,redirect
from django.urls.resolvers import URLResolver

def test(request):
    return redirect('/myadmin/showdata/video')