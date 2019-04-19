import pymysql
from bili_spider.get_video import GVI

av_num = 38450273
video_data = GVI(aid = av_num)

# print('信息', video_data.video_info)
# print('类别', video_data.video_type)
# print('作者',video_data.author )
# print('标签', video_data.dynamic_list)

conn = pymysql.connect(
    port = 3306,
    host = '127.0.0.1',
    user = 'root',
    database = 'bilibili_sql',
    charset = 'utf8'
)
cur = conn.cursor()

#关于添加信息的SQL语句

add_type = 'insert into showdata_category(tid,tname) value(%s, %s)'
add_author = 'insert into showdata_author(mid,name) value(%s, %s)'
add_tag = 'insert into showdata_tag(name) value(%s)'

add_video_tag = 'insert into showdata_video_tag(video_id, tag_id) value(%s, %s)'
add_info = "insert into showdata_video(title,aid,views,danmaku,favourit,coin,likes,author_id,category_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

#查找信息的SQL语句
search_video = 'select id from showdata_video where aid=%s'
search_tag = 'select id from showdata_tag where name=%s'


#先添加被关联的表， 在添加主表信息，和多对多表
cur.execute(add_type, [video_data.video_type.get('tid'), video_data.video_type.get('tname')])
print('添加类别完成')
cur.execute(add_author, [video_data.author.get('mid'), video_data.author.get('name')])
print('添加作者完成')
for dynamic in video_data.dynamic_list:
    cur.execute(add_tag, dynamic)
conn.commit()
print('添加标签完成')

#视频信息列表
add_info_list = video_data.video_info_list() + [video_data.author.get('mid'), video_data.video_type.get('tid')]
print(add_info_list)
cur.execute(add_info, add_info_list)
conn.commit()


#找到标签ID和视频ID， 添加到多对多中间表中
cur.execute(search_video, video_data.video_info.get('aid'))
video_id = cur.fetchone()[0]
print(video_id)
print(type(video_id))
for dynamic in video_data.dynamic_list:
    cur.execute(search_tag, dynamic)
    tag_id = cur.fetchone()[0]
    print(tag_id)
    print(type(tag_id))
    cur.execute(add_video_tag, [video_id, tag_id])

conn.commit()
cur.close()
conn.close()
print('添加信息完成')






