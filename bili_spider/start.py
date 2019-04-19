from bili_spider.insert_video import ISVI
from bili_spider.get_video import GVI
import time
import threadpool




# spawn_list = []
# for aid in range(40000000, 40000218):
#     spawn_list.append(gevent.spawn(get_and_insert, aid))

#使用协程池限制并发数量
# pool = Pool(10)
# for aid in range(40000000, 40000218):
#
#     pool.spawn(get_and_insert, aid)

def get_and_insert(aid):
    video_data = GVI(aid=aid)
    if video_data.data:
        obj = ISVI(gvi_obj=video_data)
        res = obj.insert_all()

#爬虫开始
def run(begin, end):
    if isinstance(begin, int) and isinstance(end, int):
        if end > begin and begin > 0:
            left = begin
            while left <= end:
                pool = threadpool.ThreadPool(15)
                right = left + 500
                id_list = range(left, right)
                task_list = threadpool.makeRequests(get_and_insert, id_list)
                [pool.putRequest(task) for task in task_list]
                pool.wait()
                left = right
        else:
            raise ValueError('两个参数必须大于0并且第一个小于第二个')
    else:
        raise TypeError('参数类型必须是int')

if __name__ == '__main__':
    # a = input('开始ID为', )
    # b = input('结束ID为', )
    try:
        a = 45478524
        b = 49874358
        one = time.time()
        run(a, b)
        print('完成时间为', time.time() - one)
    except TypeError as e :
        print(e)
