# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from config import API, IS_PUSH_TO_STOCK
from tools.log import Log, log_request

class StockMixin(object):

    @gen.coroutine
    def notify_stock(self, chain_id, chain_hotel_id):
        if not IS_PUSH_TO_STOCK:
            raise gen.Return()

        url = '{}/stock2/internal/hotel/update_time?chainId={}&chainHotelId={}'.format(API['STOCK'], chain_id, chain_hotel_id)

        resp = yield AsyncHTTPClient().fetch(url)
        Log.info(resp.body)
        raise gen.Return()
