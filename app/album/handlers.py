"""
@Time : 2024-06-16 19:25
@Author : rainmon
@File : handlers.py
@Project : StudyNotes-Python
@feature : 
@description：
"""

import re

import pandas as pd
from pymysql.converters import escape_item

from db.db_handler import db_handler
from base.base_handler import BaseHandler


class AlbumsQueryHandler(BaseHandler):

    async def post(self):
        if self.need_roles:
            print('需要权限')
        try:
            artists: list = self.json_args.get('artists', [])
            page_index = self.json_args.get('page_index', 1)
            page_size = self.json_args.get('page_size', 10)
            page_index = int(page_index)
            page_size = int(page_size)
            conditon = ''
            if artists:
                conditon += f" and artist in {escape_item(artists, charset='utf8')}"
            sql = f"""
            select id, title, artist, price from album where 1 = 1 {conditon}
            limit {(page_index - 1) * page_size}, {page_size}
            """
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            df['price'] = pd.to_numeric(df['price'])
            df = df.where(pd.notna(df), None)
            self.return_response(data=df.to_dict('records'))
        except Exception as e:
            self.return_response(code='500', message=f"server error: {str(e)}")


class AlbumsHandler(BaseHandler):
    async def post(self):
        try:
            if not self.json_args or set(self.json_args).difference(['title', 'artist', 'price']):
                raise ValueError('参数错误')
            sql = """
            insert album ({}) values ({})
            """.format(','.join(self.json_args.keys()), ','.join(['%s'] * len(self.json_args)))
            await db_handler.get_mysql_coroutine('study').execute_single(sql, list(self.json_args.values()))
            self.return_response(message="新增成功")
        except Exception as e:
            self.return_response(code='500', message=f"Error: {str(e)}")


class AlbumsDeleteHandler(BaseHandler):
    async def post(self):
        try:
            if not self.json_args or set(self.json_args).difference(['ids']):
                raise ValueError('参数错误')
            sql = """delete from album where id in {}
            """.format(escape_item(self.json_args['ids'], 'utf8'))
            await db_handler.get_mysql_coroutine('study').execute_single(sql)
            self.return_response(message="删除成功")
        except Exception as e:
            self.return_response(code='500', message=f"Error: {str(e)}")


class ArtistsOptions(BaseHandler):

    async def get(self, artist_key=''):
        try:
            sql = """
            select distinct artist from album where 1 = 1 
            """
            if artist_key:
                sql += f" and artist regexp {escape_item(re.escape(artist_key), 'utf8')}"
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            artists = df['artist'].dropna().unique().tolist()
            self.return_response(message="查询成功", data=artists)
        except Exception as e:
            self.return_response(code='500', message=f"Error: {str(e)}")


class AlbumsCount(BaseHandler):

    async def post(self):
        try:
            artists: list = self.json_args.get('artists', [])
            if not isinstance(artists, list):
                raise ValueError("请求参数不合法")
            condition = ''
            if artists:
                condition += f" and artist in {escape_item(artists, charset='utf8')}"
            sql = f"""
            select count(1) as total from album where 1 = 1 {condition}
            """
            df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
            self.return_response(message="查询成功", data=int(df.loc[0, 'total']))
        except Exception as e:
            self.return_response(code='500', message=f"Error: {str(e)}")
