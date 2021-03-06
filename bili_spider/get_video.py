import requests
import json
#发送请求，获取视频信息

# aid = '42939742'
# video_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
# user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
# res = requests.get(url = video_url, headers = user_agent)

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
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
    need_field = ['title', 'aid', 'view', 'danmaku', 'favorite', 'coin', 'like']
    def __init__(self, aid):
        self.url = video_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
        self.response = requests.get(url=video_url, headers=self.user_agent)
        self._info_dict = json.loads(self.response.text)
        self.data = self._info_dict.get('data')

    @property
    def video_type(self):
    #视频类别字典
        t = {}
        t['tid'] = self.data.get('tid')
        t['tname'] = self.data.get('tname')
        return t

    @property
    def video_info(self):
        #视频信息字典
        v = {}
        v['title'] = self.data.get('title')
        all_info = dict(v, **self.data.get('stat'))
        return all_info

    def video_info_list(self):
        res = []
        for field in self.need_field:
            res.append(self.video_info.get(field))
        return res

    @property
    def author(self):
        #作者字典
        a = {}
        a['mid'] = self.data.get('owner').get('mid')
        a['name'] = self.data.get('owner').get('name')
        return a

    @property
    def dynamic_list(self):
        #标签字典
        d_str = self.data.get('dynamic')
        #print(self._data)
        d_list = [i for i in d_str.split('#') if i and len(i) < 10]
        #print(d_list)
        return d_list

if __name__ == "__main__":
    res_obj = GVI(35987154)
    #print(res_obj.data)
    if res_obj.data:
        print('信息', res_obj.video_info)
        print(res_obj.video_info_list(), res_obj.video_info_list()[0])
        print(type(res_obj.video_info_list()[0]))
        print('类别', res_obj.video_type)
        print('作者',res_obj.author )
        print('标签', res_obj.dynamic_list)
    else:
        print('视频不见了')