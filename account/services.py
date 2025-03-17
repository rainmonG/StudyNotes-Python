#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/17 22:16
# @Author : rainmonG
# @File : services.py
from account.models import UserIn, UserInDB

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print('User saved!..not really')
    return user_in_db