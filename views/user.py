# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.user import UserModel

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION


class UserManagerHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin)
    def get(self):
        self.render_user_manger_page()

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def post(self):
        user = ObjectDict(json_decode(self.request.body))
        print user

        if not self.valid_new_user(user.username, user.password, user.nickname, user.department, user.permission):
            self.finish_json(errcode=400, errmsg="invalid arguments")

        else:
            _user = UserModel.get_user_by_username(self.db, user.username)

            if _user is not None:

                print 'username has been used'
                self.finish_json(errcode=400, errmsg="exist username")
            else:

                try:
                    _user = UserModel.add_user(
                        self.db, user.username, user.password, user.nickname, user.department, user.permission)
                    self.finish_json(result=_user.tojson())
                except Exception, e:
                    print e
                    self.finish_json(errcode=507, errmsg=str(e))

    @auth_login()
    @auth_permission(PERMISSIONS.admin, json=True)
    def delete(self, user_id):
        try:
            UserModel.delete_by_id(self.db, user_id)
            self.finish_json()
        except Exception, e:
            print e
            self.finish_json(errcode=200, errmsg=str(e))

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def put(self, user_id):
        data = json_decode(self.request.body)

        if not self.valid_new_user(data['username'], data['password'], data['nickname'], data['department'], data['permission']):
            self.finish_json(errcode=400, errmsg='wrong argument')
            return
        else:
            user = UserModel.get_user_by_id(self.db, user_id)
            if user is None:
                self.finish_json(errcode=404, errmsg="user id not exist")
                return
            else:

                tmp_user = UserModel.get_user_by_username(
                    self.db, data['username'])
                if tmp_user and (tmp_user.id != int(user_id)):
                    print 'exist username'
                    self.finish_json(errcode=409, errmsg="username exist")
                    return

                try:
                    UserModel.update_by_id(self.db, user_id, data['username'], data[
                                           'password'], data['nickname'], data['department'], data['permission'])
                    self.finish_json()
                    return
                except Exception, e:
                    print e
                    self.finish_json(errcode=507, errmsg=str(e))
                    return

    def render_user_manger_page(self, **kwargs):
        users = UserModel.get_users(self.db)

        users_json = json_encode([
            dict(id=user.id,
                 username=user.username,
                 password=user.password,
                 nickname=user.nickname,
                 department=user.department,
                 permission=user.permission)
            for user in users])

        self.render("user_manager.html", users=users,
                    users_json=users_json, nav=NAVIGATION.USERMANAGER, **kwargs)

    def valid_new_user(self, username, password, nickname, department, permission):
        if username and password and nickname and department:
            if len(username) > 0 and len(username) <= 20 \
                and len(password) > 0 and len(password) <= 50 \
                and len(nickname) > 0 and len(nickname) <= 20 \
                    and len(department) > 0 and len(department) <= 20:
                    return True

        return False
