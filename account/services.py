#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/17 22:16
# @Author : rainmonG
# @File : services.py
from hashlib import sha256

from account.schemas import UserIn, UserInDB, UserOut
from db.mysql_util import get_session
from db.models import User

def password_hasher(raw_password: str):
    return sha256(raw_password.encode()).hexdigest()


def save_user(user_in: UserIn):
    hashed_password = password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    user = User(**user_in_db.model_dump())
    with get_session() as session:
        session.add(user)
        session.commit()
    return user


if __name__ == '__main__':
    test_user = UserIn(
        username='test3',
        password='test3',
        roles=['normal', 'spec']
    )
    print(UserOut.model_validate(save_user(test_user)))