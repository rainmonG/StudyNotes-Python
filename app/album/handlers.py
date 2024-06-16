"""
@Time : 2024-06-16 19:25
@Author : rainmon
@File : handlers.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from ast import literal_eval

import pandas as pd
import tornado
from pymysql.converters import escape_item
from base.db.aio_mysql_util import AioMysqlHandler


class AlbumsHandler(tornado.web.RequestHandler):

    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

    async def get(self, *args, **kwargs):
        handler = AioMysqlHandler()
        try:
            print(f"收到请求：{self.request.host}")
            artists: list = literal_eval(self.get_query_argument("artists"))
            sql = """
            select * from album where 1 = 1 
            """
            if artists:
                sql += f" and artist in {escape_item(artists, charset='utf8')}"
            df = await handler.query_pd(sql)
            print('异步done')
            df['price'] = pd.to_numeric(df['price'])
            df = df.where(pd.notna(df), None)
            self.set_status(200)
            self.write({"message": "查询成功", "data": df.to_dict('records')})
        except Exception as e:
            print("query error", e)
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
