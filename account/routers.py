#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/17 22:13
# @Author : rainmonG
# @File : routers.py
from fastapi import APIRouter

from account.schemas import UserIn, UserOut
from account.services import save_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = save_user(user_in)
    return user_saved
