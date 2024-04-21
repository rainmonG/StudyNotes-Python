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
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

from configs.util import Configs


class MysqlHandler:

    def __init__(self, db: str = 'study'):
        """
        初始化数据库连接
        :param db: 数据库名
        """
        conf = Configs()
        config = conf.get_mysql_conf()
        self.engine = create_engine(
            f"mysql+mysqldb://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{db}")

    def execute_sqls(self, sqls: list):
        """
        执行DDL
        :param sqls: DDL列表
        :return:
        """
        with self.engine.begin() as conn:
            try:
                for sql in sqls:
                    conn.execute(text(sql))
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
            data.columns = [c.lower() for c in data.columns]
            return data


if __name__ == '__main__':
    handler = MysqlHandler()
    metadata_obj = MetaData()
    user_table = Table(
        "user_account",
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('fullname', String)
    )
    address_table = Table(
        "address",
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('user_id', ForeignKey('user_account.id'), nullable=False),
        Column('email_address', String, nullable=False)
    )
    print(user_table.c)
    print(user_table.primary_key)
