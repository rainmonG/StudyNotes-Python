"""
@Time : 2024-09-05 23:29
@Author : rainmon
@File : base_handler.py
@Project : StudyNotes-Python
@feature : 
@description：
"""

import tornado
from pymysql.converters import escape_str

from db.db_handler import db_handler


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, raw_uri):
        self.raw_uri = raw_uri

    async def prepare(self):
        sql = '''select role from t_uri_info where raw_uri = {} and request_method = {}'''.format(
            escape_str(self.raw_uri), escape_str(self.request.method)
        )
        df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
        if df.empty:
            self.need_roles = []
        else:
            self.need_roles = df['role'].tolist()
        print(self.need_roles)

    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")