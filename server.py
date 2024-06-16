"""
@Time : 2024-06-16 19:20
@Author : rainmon
@File : server.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import tornado
import app.album.urls as album

handlers = (
    album,
)
mapping_list = [(h['url'], h['handler']) for u in handlers for h in u.URLS]


def main():
    # 定义请求的路径和响应的请求类，此类会根据你发出的请求区分get 还是post而给予不同的处理
    application = tornado.web.Application(mapping_list)
    # 绑定端口，单进程启动
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
