"""
@Time : 2024-07-13 01:55
@Author : rainmon
@File : db_handler.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from base.db.aio_mysql_util import AioMysqlHandler
from base.db.mysql_util import MysqlHandler


class DBHelper:
    def __init__(self):
        self._mysql_sync = {}
        self._mysql_async = {}

    def get_mysql_handler(self, db: str) -> MysqlHandler:
        if not self._mysql_sync.get(db):
            self._mysql_sync[db] = MysqlHandler(db)
        return self._mysql_sync[db]

    def get_mysql_coroutine(self, db: str) -> AioMysqlHandler:
        if not self._mysql_async.get(db):
            self._mysql_async[db] = AioMysqlHandler(db)
        return self._mysql_async[db]


db_handler = DBHelper()
