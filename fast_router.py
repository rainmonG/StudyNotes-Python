"""
@Time : 2024-07-28 22:29
@Author : rainmon
@File : fast_router.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from fastapi import APIRouter

from account import user


router = APIRouter()
router.include_router(user.router)