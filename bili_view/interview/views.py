from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from json.decoder import JSONDecodeError
import time
import json
import re

# Create your views here.

def get_interview_index(request):
    return render(request, "interview_index.html")


class Add(View):
    def get(self, request):
        return render(request, "interview_nums.html")

    def post(self, request):
        res = {'status': True, 'result': None}
        nums_list = request.POST.get("value_array")
        nums_list = json.loads(nums_list)
        print(nums_list)
        print(type(nums_list))
        finish = 0
        for nums_dict in nums_list:
            print(nums_dict)
            print(type(nums_dict))
            num = nums_dict.get('value')
            if num:
                print('the num is >>>>>>>>>>', num)
                print('the type is >>>>>>>>>>', type(num))
                try:
                    num = json.loads(num)
                    if isinstance(num, int):
                        print(type(num))
                        finish += num
                except JSONDecodeError as a:
                    num = num[0]
                    try:
                        num = json.loads(num)
                        if isinstance(num, int):
                            finish += num
                    except JSONDecodeError as e:
                        res['status'] = False
                        res['result'] = '请正确数据格式'
                        break

        #print(finish)
        if res['status']:
            res['result'] = finish
        return HttpResponse(json.dumps(res))

class Date(View):

    def get(self, request):
        res = {}
        try:
            from time import struct_time
            xx = time.localtime()
            print(type(xx))
            print(xx.tm_year)
            print(xx.tm_mon)
            print(xx.tm_mday)
            print(xx.tm_hour)
            print(xx.tm_min)
            print(xx.tm_sec)
            date = '%s-%s-%s'%(xx.tm_year, xx.tm_mon, xx.tm_mday)
            tt = '%s-%s-%s'%(xx.tm_hour, xx.tm_min, xx.tm_sec)
            res['date'] = date
            res['tt'] = tt
        except Exception as e:
            print(e)
        return render(request, 'interview_date.html', {'res': res})


class Chat(View):

    def get(self, request):
        return render(request, "interview_chat.html")

    def post(self, request):
        anwser_dict = {'您好': '您好，您吃了吗？', '再见': '回见了您内。', 'both': '天气不错。'}
        #匹配结果及个数
        alive_dict = {}
        alive_count = 0
        #返回结果
        res = {}
        data = request.POST.get('msg')
        #print(data)
        if data:
            for key, anwser in anwser_dict.items():
                is_alive = re.findall(key, data)
                if is_alive:
                    print('匹配到一个')
                    alive_dict[key] = True
                    alive_count += 1
                    res['result'] = anwser
            print(alive_count)
            if alive_count > 1:
                print('匹配到多个')
                res['result'] = anwser_dict['both']
            elif alive_count == 0:
                res['result'] = '这超出了我的能力范围'
        else:
            res['result'] = '我听不见'

        print(json.dumps(res))
        return HttpResponse(json.dumps(res))