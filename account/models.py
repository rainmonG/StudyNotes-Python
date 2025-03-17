"""
@Time : 2024-07-28 22:23
@Author : rainmon
@File : models.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import enum

from pydantic import BaseModel, EmailStr, conlist


class RoleType(enum.Enum):
    ADMIN = "admin"
    NORMAL = "normal"
    SPEC = "spec"

class UserBase(BaseModel):
    uid: str
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    roles: conlist(RoleType, min_length=0) = []

    class Config:
        use_enum_values = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
