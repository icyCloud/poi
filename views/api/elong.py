# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from views.base import BtwBaseHandler
from config import API

class ElongAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self, hotel_id):
        yield self.notify_update(hotel_id)
        self.finish_json()

    @gen.coroutine
    def notify_update(self, hotel_id):
        url = '{}/elongHotelService/push/{}'.format(API['ELONG'], hotel_id)
        resp = yield AsyncHTTPClient().fetch(url)
        raise gen.Return([])
