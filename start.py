from insert_video import ISVI
from get_video import GVI
import gevent
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import pymysql



def get_and_insert(aid):
    video_data = GVI(aid=aid)
    if video_data.data:
        obj = ISVI(gvi_obj=video_data)
        res = obj.insert_all()

# spawn_list = []
# for aid in range(40000000, 40000218):
#     spawn_list.append(gevent.spawn(get_and_insert, aid))

#使用协程池限制并发数量
pool = Pool(10)
for aid in range(40000000, 40000218):

    pool.spawn(get_and_insert, aid)
