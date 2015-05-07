# -*- coding: utf-8 -*-

import traceback
import json

from tornado import gen
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tools.json import json_encode
from tools.log import Log

from views import BaseHandler
from models.user import UserModel
from exception.json_exception import JsonException, JsonDecodeError
from tornado.util import ObjectDict
from constants import Login
from tools.auth import mapping_permission
from config import DEBUG, BACKSTAGE_USERNAME_KEY
from tools.log import Log


class BtwBaseHandler(BaseHandler):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.current_user = None
        self.user_permission = 0
        self.db = self.application.DB_Session()

    def on_finish(self):
        self.db.close()

    @gen.coroutine
    def prepare(self):
        yield self.get_current_user()

    @gen.coroutine
    def get_current_user(self):
        username = self.get_secure_cookie(BACKSTAGE_USERNAME_KEY)
        if DEBUG:
            username = 'admin'

        if username:
            self.current_user = username
            self.current_user_permission = yield self.get_user_permission(username)
        raise gen.Return(self.current_user)

    @gen.coroutine
    def get_user_permission(self, username):
        url = Login.PERMISSION_URL.format(username)
        resp = yield AsyncHTTPClient().fetch(url)
        r = json.loads(resp.body)
        print r
        resources = r['result']['resources']
        permissions = [p['id'] for p in resources]
        print '=' * 10
        print permissions
        raise gen.Return(mapping_permission(permissions))



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
        username = self.get_secure_cookie('username')
