# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME

import cache


class UserModel(Base):

    __tablename__ = 'user'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(50), nullable=False)
    nickname = Column(VARCHAR(20), nullable=False)
    lastLogin = Column(DATETIME)
    permission = Column(INTEGER, nullable=False)
    department = Column(VARCHAR(20))
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    MC_USER_NAME  = __tablename__ + "mc_user_name"

    @classmethod
    def get_user_by_id(cls, session, id):
        return session.query(UserModel).filter(UserModel.id == id, UserModel.is_delete == 0).first()

    @classmethod
    @cache.mc_with_id(MC_USER_NAME)
    def get_user_by_username(cls, session, username):
        return session.query(UserModel).filter(UserModel.username == username, UserModel.is_delete == 0).first()

    @classmethod
    def get_user_by_username_and_password(cls, session, username, password):
        return session.query(UserModel)\
            .filter(UserModel.username == username, UserModel.password == password, UserModel.is_delete != 1)\
            .first()

    @classmethod
    def add_user(cls, session, username, password, nickname, department, permission):
        user = UserModel(
            username=username, password=password, nickname=nickname,
            permission=permission, department=department, is_delete=0)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_users(cls, session):
        return session.query(UserModel)\
            .filter(UserModel.is_delete == 0)\
            .all()

    @classmethod
    def delete_by_id(cls, session, id):
        user = cls.get_user_by_id(session, id)
        if user:
            user.is_delete = 1
            session.commit()
            cache.delete(cache.join_keys(cls.MC_USER_NAME, user.username))


    @classmethod
    def delete_by_username(cls, session, username):
        user = UserModel.get_user_by_username(session, username)
        if user:
            user.is_delete = 1
            session.commit()
            cache.delete(cache.join_keys(cls.MC_USER_NAME, user.username))


    @classmethod
    def update_by_id(cls, session, id, username, password, nickname, department, permission):
        user = UserModel.get_user_by_id(session, id)
        if user:
            user.username = username
            user.password = password
            user.nickname = nickname
            user.department = department
            user.permission = permission
            session.commit()
            cache.delete(cache.join_keys(cls.MC_USER_NAME, user.username))
        user = UserModel.get_user_by_id(session, id)
        print user.tojson()
        return user

    def tojson(self):
        return dict(
            id = self.id,
            username=self.username,
            password=self.password,
            nickname=self.nickname,
            department=self.department,
            permission=self.permission)
