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
        'name': 'album查询',
        'url': r'/album',
        'handler': AlbumsHandler
    },
    {
        'name': 'artists选项',
        'url': r'/artists',
        'handler': ArtistsOptions
    }
]
