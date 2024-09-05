"""
@Time : 2024-06-16 17:29
@Author : rainmon
@File : aio_mysql_util.py
@Project : StudyNotes-Python
@feature : 
@description：
"""

import pandas as pd
import aiomysql
from configs.util import Configs


class AioMysqlHandler:
    """
    __init__方法不能使用异步，所以获取连接的操作单独使用单例模式创建连接，每次进行查询时，都重新获取一个新的链接Connection
    """
    def __init__(self, db: str = 'study'):
        self.db = db
        self.pool = None

    async def init_pool(self):
        """
        初始化连接池，连接池的意义在于，保持指定数量的可用连接，当一个查询执行前从池子中取一个连接，查询结束后将连接放回池子中，避免频繁连接数据库
        :return: 连接池
        """
        config = Configs.get_mysql_conf()
        self.pool = await aiomysql.create_pool(
            host=config['host'],
            port=int(config['port']),
            user=config['user'],
            password=config['password'],
            db=self.db
        )

    async def query_pd(self, sql: str, param: list = None):
        """
        从空闲池获取连接的协程，根据需要创建新连接
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, param)
                res = await cur.fetchall()
                await conn.commit()
                data = pd.DataFrame(res, columns=[c[0] for c in cur.description])
                return data

    async def execute_sqls(self, sqls: list):
        """
        执行DDL
        :param sqls: DDL列表
        :return:
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                data = None
                try:
                    for sql in sqls:
                        await cur.execute(sql)
                        if cur.description:
                            res = await cur.fetchall()
                            data = pd.DataFrame(res, columns=[c[0] for c in cur.description])
                    await conn.commit()
                    return data if data else cur
                except Exception as e:
                    await conn.rollback()
                    raise e

    async def execute_many(self, sql: str, data: pd.DataFrame):
        if not data.empty:
            data = data.where(pd.notna(data), None)
            if not self.pool:
                await self.init_pool()
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                    try:
                        await cur.executemany(sql, data.values.tolist())
                        await conn.commit()
                    except Exception as e:
                        await conn.rollback()
                        raise e
