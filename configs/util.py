"""
@Time : 2024/4/18 22:54
@Author : rainmon
@File : util.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from configparser import ConfigParser


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class Configs:
    def __init__(self):
        self._config = ConfigParser()  # 创建对象
        self._config.read('server.ini', encoding="utf-8")  # 读取配置文件

    def get_mysql_conf(self) -> dict:
        return {
            'host': self._config.get('mysql', 'host'),
            'user': self._config.get('mysql', 'user'),
            'password': self._config.get('mysql', 'password'),
        }


if __name__ == '__main__':
    conf = Configs()
    config = conf.get_mysql_conf()
    print(config['host'])
