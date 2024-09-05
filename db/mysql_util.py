"""
@Time : 2024/4/18 23:29
@Author : rainmon
@File : mysql_util.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import pandas as pd
from sqlalchemy import create_engine, text

from configs.util import Configs


class MysqlHandler:

    def __init__(self, db: str = 'study'):
        """
        初始化数据库连接
        :param db: 数据库名
        """
        config = Configs.get_mysql_conf()
        self.engine = create_engine(
            f"mysql+mysqldb://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{db}")

    def execute_sqls(self, sqls: list):
        """
        执行DDL
        :param sqls: DDL列表
        :return:
        """
        with self.engine.begin() as conn:
            df = None
            res = None
            try:
                for sql in sqls:
                    res = conn.execute(text(sql))
                    if res.returns_rows:
                        df = pd.DataFrame(res.fetchall(), columns=list(res.keys()))
                return res if df is None else df
            except Exception as e:
                conn.rollback()
                raise e

    def query_pd(self, sql: str):
        """
        查询得到df
        :param sql:
        :return:
        """
        with self.engine.begin() as conn:
            data = pd.read_sql_query(sql, conn)
            return data


if __name__ == '__main__':
    handler = MysqlHandler()
    sqls = [
            "select 1 as test1;", "select 2 as test2;"
            ]
    print(handler.execute_sqls(sqls))
