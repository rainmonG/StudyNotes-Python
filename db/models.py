#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/17 21:30
# @Author : rainmonG
# @File : schemas.py
import uuid
from typing import List
from sqlalchemy import ForeignKey, String, Column, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "t_user"

    uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: str = Column(String(15), nullable=False)
    email: str = Column(String(100))
    fullname: str = Column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(128))

    roles: Mapped[List["UserRole"]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )

    def __init__(self, **kw):
        roles = kw.pop("roles")
        super().__init__(**kw)
        if roles:
            self.roles = [UserRole(role=_) for _ in roles]


class UserRole(Base):
    __tablename__ = "user_role"

    uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("t_user.uid", ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint("role", "user_id", name="uix_role"),
    )

