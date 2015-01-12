# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from models.user import UserModel

from tools.auth import auth_login

class LoginHandler(BtwBaseHandler):
    '''
    前期测试 密码明文
    '''

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_body_argument("username", None)
        password = self.get_body_argument("password", None)
        print "username", username
        print "password", password

        if self.valid_login(username, password):
            self.login_success()
        else:
            self.show_invalid_login(username)


    def show_invalid_login(self, username):
            self.render("login.html", error_msg="Wrong username or password", username=username)


    def valid_login(self, username, password):
        if username and password:
            user = UserModel.get_user_by_username_and_password(self.db, username, password)
            if user:
                self.current_user = user
                return True

        return False

    
    def login_success(self):
        self.set_secure_cookie("username", self.current_user.username, expires_days=0.02)
        self.redirect('/')

        



class LogoutHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.clear_all_cookies()
        self.redirect("/login/")
