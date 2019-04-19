


bili_spider(B站视频信息爬虫程序)
        get_video 爬取视频信息
        insert_videw 存储到MySQL
        start.run 爬虫开始(两个参数: 开始和结束视频ID号)
  
bili_view(Django视频信息展示)
        logres 登录注册组件
        myadmin 通用数据管理组件
        showdata 提供数据给myadmin
        
数据库设置(MySQL):
        本地创建数据库名为：bilibili_sql
        利用makemigrations和migrate创建表结构
        
