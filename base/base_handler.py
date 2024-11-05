"""
@Time : 2024-09-05 23:29
@Author : rainmon
@File : base_handler.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import json
from datetime import datetime

import tornado
from pymysql.converters import escape_str

from db.db_handler import db_handler


class BaseHandler(tornado.web.RequestHandler):
    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

    def initialize(self, raw_uri):
        self.raw_uri = raw_uri
        self.json_args = {}
        self.need_roles = []

    async def prepare(self):
        print(f"收到{self.request.remote_ip}请求：{tornado.escape.url_unescape(self.request.uri)}")
        sql = '''select role from t_uri_info where raw_uri = {} and request_method = {}'''.format(
            escape_str(self.raw_uri), escape_str(self.request.method)
        )
        df = await db_handler.get_mysql_coroutine('study').query_pd(sql)
        if df.empty:
            self.need_roles = []
        else:
            self.need_roles = df['role'].tolist()
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args.update(json.loads(self.request.body))
        for k in self.request.arguments:
            if k.endswith('[]'):
                self.json_args.update({k[:-2]: self.get_arguments(k)})
            else:
                self.json_args.update({k: self.get_argument(k)})

    def return_response(self, code: str = '200', message: str = 'Success', data=''):
        self.write({
            'code': code,
            'message': message,
            'data': data
        })

    def on_finish(self):
        inserts = {
            'remote_ip': self.request.remote_ip,
            'request_path': tornado.escape.url_unescape(self.request.path),
            'request_method': self.request.method,
            'request_args': str(self.json_args),
            'insert_time': datetime.now()

        }
        sql = '''insert into t_interface_access ({}) values ({})
        '''.format(','.join(inserts.keys()), ','.join(['%s'] * len(inserts)))
        tornado.ioloop.IOLoop.current().add_callback(
            lambda: db_handler.get_mysql_coroutine('study').execute_single(sql, list(inserts.values())))
