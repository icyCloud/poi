# -*- coding: utf-8 -*-

import traceback

from tornado.escape import json_decode
from tools.json import json_encode
from tools.log import Log

from views import BaseHandler
from models.user import UserModel
from exception.json_exception import JsonException, JsonDecodeError
from tornado.util import ObjectDict



class BtwBaseHandler(BaseHandler):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.current_user = None
        self.db = self.application.DB_Session()

    def on_finish(self):
        self.db.close()

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
        self.db.rollback()
        if isinstance(e, JsonException):
            Log.error(e.tojson)
            self.finish_json(errcode=e.errcode, errmsg=e.errmsg)
        else:
            Log.error(traceback.format_exc())
            super(BtwBaseHandler, self)._handle_request_exception(e)

    def finish_json(self, errcode=0, errmsg=None, result=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json_encode({'errcode': errcode,
                    'errmsg': errmsg,
                    'result': result}))


    def get_json_arguments(self, raise_error=True):
        try:
            return ObjectDict(json_decode(self.request.body))
        except Exception, e:
            print traceback.format_exc()
            if raise_error:
                raise JsonDecodeError()

class StockHandler(BtwBaseHandler):
    def initialize(self):
        super(StockHandler, self).initialize()
        self.db_stock = self.application.DB_Session_stock()

    def on_finish(self):
        super(StockHandler, self).on_finish()
        self.db_stock.close()
