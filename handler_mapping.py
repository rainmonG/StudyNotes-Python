"""
@Time : 2024-09-05 23:22
@Author : rainmon
@File : handler_mapping.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from tornado.web import url

import app.album.urls as album

__handlers = (
    album,
)
handlers = [url(h['url'], h['handler'], dict(raw_uri=h['url']), name=h['name']) for u in __handlers for h in u.URLS]
