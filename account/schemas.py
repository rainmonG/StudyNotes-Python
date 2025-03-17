"""
@Time : 2024-07-28 22:23
@Author : rainmon
@File : schemas.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import enum
from typing import Any, Self

from pydantic import BaseModel, EmailStr, conlist


class RoleType(enum.Enum):
    ADMIN = "admin"
    NORMAL = "normal"
    SPEC = "spec"

class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    fullname: str | None = None
    roles: conlist(RoleType, min_length=0) = []

    class Config:
        use_enum_values = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    uid: str

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
    ) -> Self:
        return UserOut(
            uid=obj.uid.hex,
            username=obj.username,
            email=obj.email,
            fullname=obj.fullname,
            roles=[_.role for _ in obj.roles],
        )



class UserInDB(UserBase):
    hashed_password: str
