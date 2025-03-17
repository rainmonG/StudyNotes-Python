#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/17 22:16
# @Author : rainmonG
# @File : services.py
from hashlib import sha256
from sqlalchemy import select, update

from account.schemas import UserIn, UserInDB, UserOut
from db.mysql_util import get_session
from db.models import User, UserRole

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
    # test_user = UserIn(
    #     username='test3',
    #     password='test3',
    #     roles=['normal', 'spec']
    # )
    # print(UserOut.model_validate(save_user(test_user)))
    with get_session() as session:
        session.query(UserRole).delete()
        session.commit()
        sql = select(User)
        users = session.execute(sql).scalars().all()
        for orig_user in users:
            print(orig_user.username, orig_user.uid)
            if orig_user.username.startswith('test1'):
                session.add(UserRole(user_id=orig_user.uid, role='normal'))
            elif orig_user.username.startswith('test2'):
                session.add(UserRole(user_id=orig_user.uid, role='spec'))
            else:
                session.add(UserRole(user_id=orig_user.uid, role='admin'))
        session.commit()