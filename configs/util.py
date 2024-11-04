"""
@Time : 2024/4/18 22:54
@Author : rainmon
@File : util.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import os

from configparser import ConfigParser

CUR_DIR = os.path.dirname(__file__)


class Configs:
    _config = ConfigParser()  # 创建对象
    _config.read(os.path.join(CUR_DIR, 'server.ini'), encoding="utf-8")  # 读取配置文件

    @classmethod
    def get_mysql_conf(cls) -> dict:
        sections = ['host', 'port', 'user', 'password']
        return {k: cls._config.get('mysql', k) for k in sections}

    @classmethod
    def get_redis_conf(cls) -> dict:
        sections = ['host', 'port']
        return {k: cls._config.get('redis', k) for k in sections}

    @classmethod
    def get_mongo_conf(cls) -> dict:
        sections = ['host', 'port', 'username', 'password', 'dbase']
        return {k: cls._config.get('mongodb', k) for k in sections}


if __name__ == '__main__':
    config = Configs.get_mysql_conf()
    print(config['host'])
