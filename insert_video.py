import pymysql
from get_video import GVI


#insert_sql_video_info
class ISVI(object):
    #连接的数据库信息
    port = 3306
    host = '127.0.0.1'
    user = 'root'
    database = 'bilibili_sql'
    password = ''
    #SQL语句(添加和查询)
    add_info = "insert into showdata_video(title,aid,views,danmaku,favourit,coin,likes,author_id,category_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    add_video_tag = 'insert into showdata_video_tag(video_id, tag_id) value(%s, %s)'

    add_type = 'insert into showdata_category(tid,tname) value(%s, %s)'
    add_author = 'insert into showdata_author(mid,name) value(%s, %s)'
    add_tag = 'insert into showdata_tag(name) value(%s)'

    search_info = "select id from showdata_video where aid=%s"
    search_type = "select tid from showdata_category where tid=%s"
    search_author = "select mid from showdata_author where mid=%s"
    search_tag = "select id from showdata_tag where name=%s"

    def __init__(self, gvi_obj):
        self._conn = pymysql.connect(
            port = self.port,
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
        )
        self._cur = self._conn.cursor()
        self.gvi = gvi_obj


    def _insert_type(self):
        res = self._cur.execute(self.search_type, self.gvi.video_type.get('tid'))
        if not res:
            self._cur.execute(self.add_type, [self.gvi.video_type.get('tid'), self.gvi.video_type.get('tname')])
        else:
            print('编号%s类别信息已存在' % self.gvi.video_type.get('tid'))

    def _insert_author(self):
        res = self._cur.execute(self.search_author, self.gvi.author.get('mid'))
        if not res:
            self._cur.execute(self.add_author, [self.gvi.author.get('mid'), self.gvi.author.get('name')])
        else:
            print('编号%s作者信息已存在' % self.gvi.author.get('mid'))

    def _insert_tag(self):
        for dynamic in self.gvi.dynamic_list:

            res = self._cur.execute(self.search_tag, dynamic)
            if not res:
                self._cur.execute(self.add_tag, dynamic)
            else:
                print('##%s##标签已存在', dynamic)

    def insert_all(self):
        try:
            res = self._cur.execute(self.search_info, self.gvi.video_info.get('aid'))
            if not res:
                self._insert_author()
                self._insert_tag()
                self._insert_type()
                self._conn.commit()
                add_info_list = self.gvi.video_info_list() + [self.gvi.author.get('mid'), self.gvi.video_type.get('tid')]
                self._cur.execute(self.add_info, add_info_list)
                self._conn.commit()
                self._cur.execute(self.search_info, self.gvi.video_info.get('aid'))
                video_id = self._cur.fetchone()[0]
                for dynamic in self.gvi.dynamic_list:
                    self._cur.execute(self.search_tag, dynamic)
                    tag_id = self._cur.fetchone()[0]
                    self._cur.execute(self.add_video_tag, [video_id, tag_id])
                self._conn.commit()
            else:
                print('视频信息已存在')
            return True
        except Exception as e:
            print(e)
            return False

        finally:
            self._cur.close()
            self._conn.close()


if __name__ == '__main__':
    av_num = 27393595
    video_data = GVI(aid=av_num)

    obj = ISVI(gvi_obj = video_data)
    res = obj.insert_all()
    if res:
        print('添加完成')
    else:
        print('添加失败')





