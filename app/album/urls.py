"""
@Time : 2024-06-16 19:24
@Author : rainmon
@File : urls.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from app.album.handlers import *

URLS = [
    {
        'name': 'album分页查询',
        'url': r'/albums',
        'handler': AlbumsHandler
    },
    {
        'name': 'album查询总计',
        'url': r'/albums_count',
        'handler': AlbumsCount
    },
    {
        'name': 'artists选项',
        'url': r'/artists_option',
        'handler': ArtistsOptions
    }
]
