"""
@Time : 2024-06-16 19:25
@Author : rainmon
@File : handlers.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import json
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

    async def post(self, *args, **kwargs):
        handler = AioMysqlHandler()
        try:
            print(f"收到新增请求：{self.request.host}")
            content_type = self.request.headers.get('content-type')
            if content_type.startswith('text/plain'):
                post_data = json.loads(self.request.body.decode())
                df = pd.Series(post_data).to_frame().T
            elif content_type.startswith('multipart/form-data'):
                post_data = {}
                for key in self.request.arguments:
                    post_data[key] = self.get_body_arguments(key)
                df = pd.DataFrame(post_data)
            else:
                self.set_status(400)
                self.write({"message": "错误请求", "data": None})
                return
            if df.empty:
                self.set_status(400)
                self.write({"message": "无新增", "data": None})
            else:
                sql = """
                insert album ({}) values ({})
                """.format(','.join(df.columns), ','.join(['%s'] * len(df.columns)))
                await handler.execute_many(sql, df)
                print('异步新增done')
                self.set_status(201)
                self.write({"message": "新增成功", "data": None})
        except Exception as e:
            print("query error", e)
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
