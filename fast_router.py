"""
@Time : 2024-07-28 22:29
@Author : rainmon
@File : fast_router.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from fastapi import APIRouter

from account.routers import router as account_routers


router = APIRouter()
router.include_router(account_routers)