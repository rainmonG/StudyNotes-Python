"""
@Time : 2024-07-28 22:23
@Author : rainmon
@File : user.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr


router = APIRouter(prefix='/users', tags=['users'])


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print('User saved!..not really')
    return user_in_db


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
