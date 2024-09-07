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
        'name': 'album新增',
        'url': r'/albums',
        'handler': AlbumsHandler
    },
    {
        'name': 'album删除',
        'url': r'/albums_delete',
        'handler': AlbumsDeleteHandler
    },
    {
        'name': 'album查询',
        'url': r'/albums_query',
        'handler': AlbumsQueryHandler
    },
    {
        'name': 'album查询总计',
        'url': r'/albums_count',
        'handler': AlbumsCount
    },
    {
        'name': 'artists模糊选项',
        'url': r'/artists_option/(?P<artist_key>.*)',
        'handler': ArtistsOptions
    }
]
