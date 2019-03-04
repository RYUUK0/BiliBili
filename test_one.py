import requests
from bs4 import BeautifulSoup
from requests.models import Response
from bs4.element import Tag
from bs4.element import Comment
import re
import json



# index_url = 'https://www.bilibili.com/'
# game_url = 'https://www.bilibili.com/v/game/'
# index_res = requests.get(
#     url = index_url
# )
#B站首页信息
#print(type(res))

# clean_data = BeautifulSoup(res.text, 'html.parser')
# one_ul_menu = clean_data.find(name = 'ul', attrs = {'class': 'nav-menu'})
# one_li_list = one_ul_menu.children
# #一级分类的li标签列表
# for li in one_li_list:
#     if not li.get('class'):
#         a_tag = li.find(name = 'a')
#         url = a_tag.get('href')
#         title = a_tag.find(name = 'div', attrs = {'class': 'nav-name'}).text
#         print('一级标题是>>>>>>>>>>>>>>>', title)
#         print('一级网址是>>>>>>>>>>>>>>>', url)
#         #在li标签对象中查找二级ul标签
#         two_url_menu = li.find(name='ul', attrs={'class': 'sub-nav'})
#         two_li_list = two_url_menu.children
#         for two_li in two_li_list:
#             if type(two_li) != Comment:
#                 url = two_li.find(name = 'a').get('href')
#                 title = two_li.find('span').text
#                 print('二级标题是>>>>>>>>>>>>', title)
#                 print('二级URL>>>>>>>>>>>>>>>', url)
#         print('#################')


#直接获取primary_menu的所有连接
#分类信息由网页静态加载，可直接爬取
# clean_data = BeautifulSoup(index_res.text, 'html.parser')
#a_list = clean_data.find(name = 'div', attrs = {'id': 'primary_menu'}).find_all(name = 'a')
#url_list = []
# for a_tag in a_list:
#     url = a_tag.get('href')
#     if 'live' not in url and url:
#         if 'http' not in url:
#             url = 'https:' + url
#         url_list.append(url)
#
# print(url_list)
# print(len(url_list))

#首页：动态加载各个类别的推荐视频，直接爬取不到
#每个页面的'class= spread-module'的div标签
#和class = groom-moudle 的div标签
# print(clean_data)
# groom_moudle_div_list = clean_data.find_all(name = 'div', attrs = {'class': 'groom-module'})
# spread_module_div_list = clean_data.find_all(name = 'div', attrs = {'class': 'spread-module'})
# print('the len of groom is ', len(groom_moudle_div_list))
# print('the len of spread is ', len(spread_module_div_list))

# all_a_tag_list = clean_data.find_all(name = 'a')
# for a_tag in all_a_tag_list:
#     aid = a_tag.get('href')
#     print(aid)
#动态加载子类别的视频
# game_res = requests.get(url = game_url)
# game_data = BeautifulSoup(game_res.text, 'html.parser')
# new = game_data.find(name = 'div', attrs = {'class' : 'spread-module'})
# print(game_data)

url = 'https://www.bilibili.com/video/av43715216'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
res= requests.get(url, headers = user_agent)
res.encoding = 'utf8'
judge = r"window\.__playinfo__=(.*?)</script>"

#print(res.text)
xxx = re.findall(judge, res.text)[0]
print(type(xxx))
#获取信息字典
json_xxx = json.loads(xxx)
# print(json_xxx)
# print(type(json_xxx))
print('############################################')
#视频地址
#print(json_xxx['data'])
the_video_url = json_xxx['data']['dash']['video']
print(the_video_url)
print(type(the_video_url))

def download(url):
    pass





