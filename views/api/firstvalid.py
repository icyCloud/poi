# -*- coding: utf-8 -*-

import time

from tornado.util import ObjectDict
from tornado import gen
from tornado.escape import json_encode, json_decode, url_escape

from views.base import BtwBaseHandler, StockHandler
from mixin.hotelmixin import HotelMixin

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.hotel import HotelModel as Hotel
from models.room_type_mapping import RoomTypeMappingModel as RoomTypeMapping
from models.room_type import RoomTypeModel as RoomType

from tools.log import Log, log_request


class FirstValidAPIHandler(StockHandler, HotelMixin):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    @log_request
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)

        provider_id = self.get_query_argument('provider_id', None)
        hotel_name = self.get_query_argument('hotel_name', None)
        city_id = self.get_query_argument('city_id', None)

        t0 = time.time()
        hotel_mappings, total = HotelMapping.gets_show_in_firstvalid(self.db,
                                                                     provider_id=provider_id, hotel_name=hotel_name, city_id=city_id,
                                                                     start=start, limit=limit)
        Log.info(">> get show in first valid")
        hotels = [hotel.todict() for hotel in hotel_mappings]

        Log.info(">> merge hotel mapping")
        t1 = time.time()
        self.merge_main_hotel_info(hotels)
        Log.info(">> merge main hotel info")
        t2 = time.time()

        self.merge_room_type_mapping(hotels)
        Log.info(">> merge roomtype mapping")
        t4 = time.time()
        self.add_provider_roomtype(hotels)
        Log.info(">> add provider roomtype mapping")
        t5 = time.time()


        cost = t1-t0, t2-t1, t4-t2, t5-t4 
        Log.info(cost)

        self.finish_json(result=dict(
            hotel_mappings=hotels,
            roomtypes=self.roomtypes,
            start=start,
            limit=limit,
            total=total))


    def merge_room_type_mapping(self, hotel_dicts):

        provider_hotel_ids = [hotel.provider_hotel_id for hotel in hotel_dicts]
        provider_hotel_ids = {}.fromkeys(provider_hotel_ids).keys()
        provider_hotel_ids.sort()

        roomtype_mappings = RoomTypeMapping.get_firstvalid_by_provider_hotel_ids(
            self.db, provider_hotel_ids)
        roomtype_mappings = [mapping.todict() for mapping in roomtype_mappings]


        main_hotel_ids = [
            mapping.main_hotel_id for mapping in roomtype_mappings]
        main_hotel_ids = {}.fromkeys(main_hotel_ids).keys()
        main_hotel_ids.sort()

        self.roomtypes = RoomType.gets_by_hotel_ids(self.db, main_hotel_ids)
        self.roomtypes = [roomtype.todict() for roomtype in self.roomtypes]

        self.merge_room_type(self.roomtypes, roomtype_mappings)
        for hotel in hotel_dicts:
            roomtype_mapping_dicts = [
                roomtype_mapping
                for roomtype_mapping in roomtype_mappings
                if hotel.provider_id == roomtype_mapping.provider_id
                and hotel.provider_hotel_id == roomtype_mapping.provider_hotel_id]
            hotel['roomtype_mappings'] = roomtype_mapping_dicts

    def merge_room_type(self, roomtypes, room_type_mapping_dicts):
        for mapping in room_type_mapping_dicts:
            for roomtype in roomtypes:
                if mapping.main_roomtype_id == roomtype.id:
                    mapping['main_roomtype'] = roomtype


class FirstValidStatusAPIHandelr(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self, hotel_mapping_id):
        Log.info("First>>Hotel {}>>Valid>> user:{}".format(hotel_mapping_id, self.current_user))
        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and\
                (hotel_mapping.status == hotel_mapping.STATUS.wait_first_valid
                 or hotel_mapping.status == hotel_mapping.STATUS.init)\
                and hotel_mapping.main_hotel_id != 0:

            hotels = HotelMapping.get_by_chain_id_and_main_hotel_id(self.db, hotel_mapping.provider_id, hotel_mapping.main_hotel_id)
            for hotel in hotels:
                if hotel.id != hotel_mapping.id and hotel.status > hotel_mapping.status:
                    self.finish_json(errcode=402, errmsg=u"已有Hotel{}绑定相同基础酒店".format(hotel.provider_hotel_name))
                    return

            r = HotelMapping.set_firstvalid_complete(self.db, hotel_mapping_id)
            self.finish_json(result=dict(
                hotel_mapping=r.todict(),
            ))
        else:
            self.finish_json(errcode=401, errmsg="not valid")


class FirstValidRoomTypeAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self, roomtype_mapping_id):
        Log.info("First>>RoomType {}>>Valid>> user:{}".format(roomtype_mapping_id, self.current_user))
        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)

        if mapping and mapping.status in [mapping.STATUS.wait_first_valid, mapping.STATUS.init]\
                and mapping.main_roomtype_id != 0:

            r = RoomTypeMapping.set_firstvalid_complete(
                self.db, roomtype_mapping_id)
            self.finish_json(result=ObjectDict(
                roomtype_mapping=r.todict(),
            ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")
