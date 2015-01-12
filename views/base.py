# -*- coding: utf-8 -*-

from tools.json import json_encode

from views import BaseHandler
from models.user import UserModel

class BtwBaseHandler(BaseHandler):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.current_user = None

    def prepare(self):
        self.get_current_user()

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        if username:
            self.set_secure_cookie('username', username, expires_days=0.02)
        self.current_user = UserModel.get_user_by_username(self.db, username)
        return self.current_user

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.current_user
        super(BtwBaseHandler, self).render(template_name, **kwargs)

    def _handle_request_exception(self, e):
        super(BtwBaseHandler, self)._handle_request_exception(e)

    def finish_json(self, errcode=0, errmsg=None, result=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json_encode({'errcode': errcode,
                    'errmsg': errmsg,
                    'result': result}))


