"""
@Time : 2024-07-13 01:55
@Author : rainmon
@File : db_handler.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import redis
from pymongo import MongoClient
from pymongo.database import Database

from db.aio_mysql_util import AioMysqlHandler
from db.mysql_util import MysqlHandler
from configs.util import Configs


class DBHelper:
    def __init__(self):
        self._mysql_sync = {}
        self._mysql_async = {}
        self._redis = {}
        self._mongodb = None

    def get_mysql_handler(self, db: str) -> MysqlHandler:
        if not self._mysql_sync.get(db):
            self._mysql_sync[db] = MysqlHandler(db)
        return self._mysql_sync[db]

    def get_mysql_coroutine(self, db: str) -> AioMysqlHandler:
        if not self._mysql_async.get(db):
            self._mysql_async[db] = AioMysqlHandler(db)
        return self._mysql_async[db]

    def get_redis(self, db: int = 0) -> redis.Redis:
        if not self._redis.get(db):
            conf = Configs.get_redis_conf()
            pool = redis.ConnectionPool(host=conf['host'], port=int(conf['port']), db=db,
                                        decode_responses=True)
            self._redis[db] = redis.Redis(connection_pool=pool)
        return self._redis[db]

    def get_mongodb(self) -> Database:
        if not self._mongodb:
            conf = Configs.get_mongo_conf()
            self._mongodb = MongoClient(host=conf['host'], port=int(conf['port']),
                                        username=conf['username'], password=conf['password'],
                                        authSource=conf['dbase'])[conf['dbase']]
        return self._mongodb


db_handler = DBHelper()


if __name__ == '__main__':
    db = db_handler.get_mongodb()
    for db_set in db.list_collections():
        print(db_set.items())

