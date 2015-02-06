# -*- coding: utf-8 -*-

import time

from tornado import gen
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient

from views.base import BtwBaseHandler

from exception.json_exception import JsonException

from tools.auth import auth_login, auth_permission
from tools.log import Log, log_request
from constants import PERMISSIONS
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.hotel import HotelModel as Hotel
from models.room_type_mapping import RoomTypeMappingModel as RoomTypeMapping
from models.room_type import RoomTypeModel as RoomType

from config import API

class EbookingAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    @log_request
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)

        hotel_name = self.get_query_argument('hotel_name', None)
        city_id = self.get_query_argument('city_id', None)

        merchant_id = self.get_query_argument('merchant_id', None)
        merchant_type = self.get_query_argument('merchant_type', None)

        merchant_ids = yield self.get_merchant_ids(merchant_type, merchant_id)
        print locals()
        if merchant_ids == []:
            self.finish_json(result=dict(
                hotel_mappings=[],
                start=start,
                limit=limit,
                total=0))
            return



        Log.info(">> get show in ebooking")
        t0 = time.time() 
        hotel_mappings, total = HotelMapping.gets_show_in_ebooking(self.db,
                hotel_name=hotel_name, city_id=city_id, merchant_ids=merchant_ids,
                start=start, limit=limit)
        t1 = time.time()
        Log.info(">> show in ebooking cost {}".format(t1 - t0))

        hotels = [hotel.todict() for hotel in hotel_mappings]
        t2 = time.time()
        self.merge_main_hotel_info(hotels)
        t3 = time.time()
        Log.info(">> merge main hotel info cost {}".format(t3 - t2))

        t4 = time.time()
        self.merge_room_type_mapping(hotels)
        t5 = time.time()
        Log.info(">> merge roomtype mapping cost {}".format(t5 - t4))

        self.finish_json(result=dict(
            hotel_mappings=hotels,
            start=start,
            limit=limit,
            total=total))

    def merge_main_hotel_info(self, hotels):
        hotel_ids = [mapping.main_hotel_id for mapping in hotels]
        main_hotels = Hotel.get_by_ids(self.db, hotel_ids)

        for hotel in hotels:
            for main_hotel in main_hotels:
                if main_hotel.id == hotel.main_hotel_id:
                    hotel['main_hotel'] = main_hotel.todict()
                    break

    def merge_room_type_mapping(self, hotel_dicts):
        provider_hotel_ids = [hotel.provider_hotel_id for hotel in hotel_dicts]
        provider_hotel_ids = self.uniq_list(provider_hotel_ids)
        roomtype_mappings = RoomTypeMapping.get_polymer_provider_hotel_ids(self.db, provider_hotel_ids)
        roomtype_mapping_dicts = [room.todict() for room in roomtype_mappings]
        
        main_roomtype_ids = [mapping.main_roomtype_id for mapping in roomtype_mappings]
        main_roomtype_ids= self.uniq_list(main_roomtype_ids)
        main_roomtypes = RoomType.get_by_ids(self.db, main_roomtype_ids)
        main_roomtype_dicts = [room.todict() for room in main_roomtypes]

        self.merge_roomtype_to_roomtype_mapping(roomtype_mapping_dicts, main_roomtype_dicts)
        self.merge_roomtype_to_hotel(hotel_dicts, roomtype_mapping_dicts)

    def merge_roomtype_to_hotel(self, hotels, roomtype_mappings):
        for hotel in hotels:
            hotel['roomtype_mappings'] = []
            for roomtype_mapping in roomtype_mappings:
                if hotel.provider_id == roomtype_mapping.provider_id\
                        and hotel.provider_hotel_id == roomtype_mapping.provider_hotel_id:
                    hotel['roomtype_mappings'].append(roomtype_mapping)

    def merge_roomtype_to_roomtype_mapping(self, roomtype_mappings, roomtypes):
        for roomtype_mapping in roomtype_mappings:
            for room in roomtypes:
                if room.id == roomtype_mapping.main_roomtype_id:
                    roomtype_mapping['main_roomtype'] = room
                    break

    def uniq_list(self, alist):
        _list = {}.fromkeys(alist).keys()
        _list.sort()
        return _list

    @gen.coroutine
    def get_merchant_ids(self, merchant_type, merchant_id):
        merchant_ids = None
        if merchant_id is not None:
            merchant_ids = [int(merchant_id)]
        elif merchant_type is not None:
            merchants = yield self.fetch_merchants()
            merchant_ids = [merchant['id'] for merchant in merchants if merchant['type'] == int(merchant_type)]
        raise gen.Return(merchant_ids)

    @gen.coroutine
    def fetch_merchants(self):
        url = API['EBOOKING'] + '/api/merchant/all/'
        resp  = yield AsyncHTTPClient().fetch(url)
        r = json_decode(resp.body)
        if r['errcode'] == 0:
            raise gen.Return(r['result']['merchants'])
        else:
            raise gen.Return([])


class MerchantListHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self):
        url = API['EBOOKING'] + '/api/merchant/all/'
        resp  = yield AsyncHTTPClient().fetch(url)
        r = json_decode(resp.body)
        if r['errcode'] == 0:
            self.finish_json(result=r['result'])
        else:
            raise JsonException(errcode=1000, errmsg="fetch merchant list fail")
