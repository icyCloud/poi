# -*- coding: utf-8 -*-

from tornado.escape import json_encode

from views.base import BtwBaseHandler


class IndexHandler(BtwBaseHandler):

    def get(self):
        self.render('index.html')
