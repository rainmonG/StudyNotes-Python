"""
@Time : 2024-06-16 19:25
@Author : rainmon
@File : handlers.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import json
import re
from ast import literal_eval

import pandas as pd
import tornado
from pymysql.converters import escape_item
from base.db.db_handler import db_handler


class AlbumsHandler(tornado.web.RequestHandler):

    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

    async def get(self):
        try:
            print(f"收到{self.request.host}请求：{self.request.full_url()}")
            self.set_status(200)
            params = {k: self.request.query_arguments[k][0].decode() for k in self.request.query_arguments}
            artists: list = literal_eval(params.get('artists'))
            page_index = int(params.get("page_index"))
            page_size = int(params.get("page_size"))
            if not isinstance(artists, list):
                self.write({"code": "400", "message": "请求参数不合法", "data": None})
                await self.finish()
                return
            conditon = ''
            if artists:
                conditon += f" and artist in {escape_item(artists, charset='utf8')}"
            sql = f"""
            select * from album where 1 = 1 {conditon}
            limit {(page_index - 1) * page_size}, {page_size}
            """
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            df['price'] = pd.to_numeric(df['price'])
            df = df.where(pd.notna(df), None)
            self.write({"code": "200", "message": "查询成功", "data": df.to_dict('records')})
        except Exception as e:
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
            await self.finish()
            raise e

    async def post(self):
        try:
            print(f"收到{self.request.host}新增请求：{self.request.full_url()}")
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
                await db_handler.get_mysql_coroutine('study').execute_many(sql, df)
                self.set_status(201)
                self.write({"message": "新增成功", "data": None})
        except Exception as e:
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
            await self.finish()
            raise e


class ArtistsOptions(tornado.web.RequestHandler):

    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET,OPTIONS")

    async def get(self):
        try:
            print(f"收到{self.request.host}请求：{self.request.full_url()}")
            self.set_status(200)
            artist_key: str = self.get_query_argument("artist_key", strip=False)
            if not isinstance(artist_key, str):
                self.write({"code": "400", "message": "请求参数不合法", "data": None})
                await self.finish()
                return
            sql = """
            select distinct artist from album where 1 = 1 
            """
            sql += f" and artist regexp {escape_item(re.escape(artist_key), 'utf8')}"
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            artists = df['artist'].dropna().unique().tolist()
            self.write({"code": "200", "message": "查询成功", "data": artists})
        except Exception as e:
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
            await self.finish()
            raise e


class AlbumsCount(tornado.web.RequestHandler):

    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET,OPTIONS")

    async def get(self):
        try:
            print(f"收到{self.request.host}请求：{self.request.full_url()}")
            self.set_status(200)
            params = {k: self.request.query_arguments[k][0].decode() for k in self.request.query_arguments}
            artists: list = literal_eval(params.get('artists'))
            if not isinstance(artists, list):
                self.write({"code": "400", "message": "请求参数不合法", "data": None})
                await self.finish()
                return
            conditon = ''
            if artists:
                conditon += f" and artist in {escape_item(artists, charset='utf8')}"
            sql = f"""
            select count(1) as total from album where 1 = 1 {conditon}
            """
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            self.write({"code": "200", "message": "查询成功", "data": int(df.loc[0, 'total'])})
        except Exception as e:
            self.set_status(500)
            self.write({"message": "server error！", "data": None})
            await self.finish()
            raise e
