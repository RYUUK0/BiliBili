import requests
#发送请求，获取视频信息

aid = '42939742'
video_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
res = requests.get(url = video_url, headers = user_agent)

#返回数据进行解析
# mess_obj = json.loads(res.text)
# for k, data in mess_obj.items():
#     #print(k)
#     #if type(data) != dict:
#         #print(data)
#     #else:
#     if type(data) == dict:
#         """
#         在data字典中:
#         tid: 类别ID
#         tname: 类别名
#         title: 标题
#         desc: 简介
#         owner: 字典，作者信息(ID, 名字)
#         stat: 字典，视频信息(
#                 aid: 视频ID,
#                 view: 播放次数,
#                 danmaku: 弹幕数量,
#                 favorite: 收藏,
#                 coin: 硬币数,
#                 like: 点赞
#             )
#         dynamic: 标签
#         """
#         print('类别ID', data.get('tid'))
#         print('类别名', data.get('tname'))
#         print('标题', data.get('title'))
#         #print('简介', data.get('desc'))
#         print('标签', data.get('dynamic'))
#         print('作者字典', data.get('owner'))
#         print('视频信息字典', data.get('stat'))

class GVI(object):
# GVI(get_video_info)类(传入requests返回值
    def __init__(self, response):
        import json
        self.response = response
        self._info_dict = json.loads(response.text)
        self._data = self._info_dict.get('data')

    @property
    def video_type(self):
    #视频类别字典
        t = {}
        t['id'] = self._data.get('tid')
        t['name'] = self._data.get('tname')
        return t

    @property
    def video_info(self):
        #视频信息字典
        v = {}
        v['title'] = self._data.get('title')
        all_info = dict(v, **self._data.get('stat'))
        return all_info

    @property
    def author(self):
        a = {}
        a['mid'] = self._data.get('owner').get('mid')
        a['name'] = self._data.get('owner').get('name')
        return a

    @property
    def dynamic_list(self):
        d_str = self._data.get('dynamic')
        d_list = [i for i in d_str.split('#') if i]
        #print(d_list)
        return d_list


res_obj = GVI(res)
print('信息', res_obj.video_info)
print('类别', res_obj.video_type)
print('作者',res_obj.author )
print('标签', res_obj.dynamic_list)