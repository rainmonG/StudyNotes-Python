"""
@Time : 2024-06-16 19:20
@Author : rainmon
@File : server.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import asyncio
import tornado

from handler_mapping import handlers


async def main():
    app = tornado.web.Application(handlers=handlers)
    app.listen(8888, '0.0.0.0')
    await asyncio.Event().wait()

if __name__ == "__main__":
    print('已于8888端口启动\nCTRL+C退出')
    asyncio.run(main())
