# -*- coding: utf-8 -*-

from tornado.util import ObjectDict
from tornado import gen
from tornado.escape import json_encode, json_decode

from views.base import BtwBaseHandler
from mixin.hotelmixin import HotelMixin

from tools.auth import auth_login, auth_permission
from tools.log import Log, log_request
from constants import PERMISSIONS
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.hotel import HotelModel as Hotel
from models.room_type_mapping import RoomTypeMappingModel as RoomTypeMapping
from models.room_type import RoomTypeModel as RoomType
from models.city import CityModel
from models.district import DistrictModel

class PolymerAPIHandler(BtwBaseHandler, HotelMixin):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    @log_request
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)

        provider_id = self.get_query_argument('provider_id', None)
        hotel_name = self.get_query_argument('hotel_name', None)
        city_id = self.get_query_argument('city_id', None)

        hotel_mappings, total = HotelMapping.gets_show_in_polymer(self.db,
                provider_id=provider_id, hotel_name=hotel_name, city_id=city_id,
                start=start, limit=limit)

        hotels = [hotel.todict() for hotel in hotel_mappings]
        self.merge_main_hotel_info(hotels)
        self.merge_room_type_mapping(hotels)
        self.add_provider_roomtype(hotels)

        self.finish_json(result=dict(
            hotel_mappings=hotels,
            roomtypes=self.roomtypes,
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
        provider_hotel_ids = {}.fromkeys(provider_hotel_ids).keys()
        provider_hotel_ids.sort()

        roomtype_mappings = RoomTypeMapping.get_polymer_provider_hotel_ids(self.db, provider_hotel_ids)

        main_hotel_ids = [mapping.main_hotel_id for mapping in roomtype_mappings]
        main_hotel_ids = {}.fromkeys(main_hotel_ids).keys()
        main_hotel_ids.sort()

        self.roomtypes = RoomType.gets_by_hotel_ids(self.db, main_hotel_ids)
        self.roomtypes =[roomtype.todict() for roomtype in self.roomtypes]


        for hotel in hotel_dicts:
            roomtype_mapping_dicts = [
                roomtype_mapping.todict()
                for roomtype_mapping in roomtype_mappings
                if hotel.provider_id == roomtype_mapping.provider_id\
                        and hotel.provider_hotel_id == roomtype_mapping.provider_hotel_id]
            self.merge_room_type(self.roomtypes, roomtype_mapping_dicts)
            hotel['roomtype_mappings'] = roomtype_mapping_dicts
            
    def merge_room_type(self, roomtypes, room_type_mapping_dicts):
        for mapping in room_type_mapping_dicts:
            for roomtype in roomtypes:
                if mapping.main_roomtype_id == roomtype.id:
                    mapping['main_roomtype'] = roomtype


class PolymerHotelAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        hotel_mapping_id = req.hotel_mapping_id
        is_online = req.is_online


        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.valid_complete:
            hotel_mapping = HotelMapping.set_online(self.db, hotel_mapping_id, is_online)
            if hotel_mapping.is_online == 0:
                RoomTypeMapping.disable_by_provider_hotel_id(self.db, hotel_mapping.provider_hotel_id)
            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def delete(self, hotel_mapping_id):
        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.valid_complete:
            hotel_mapping = HotelMapping.revert_to_firstvalid(self.db, hotel_mapping_id)
            RoomTypeMapping.revert_to_firstvalid_by_provider_hotel_id(self.db, hotel_mapping.provider_hotel_id)
            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")


class PolymerRoomTypeAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        roomtype_mapping_id = req.roomtype_mapping_id
        hotel_mapping_id = req.hotel_mapping_id
        is_online = req.is_online

        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if not hotel_mapping or hotel_mapping.is_online == 0:
            self.finish_json(errcode=402, errmsg="hotel mapping not online")
            return

        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.valid_complete:
            RoomTypeMapping.set_online(self.db, roomtype_mapping_id, is_online)
            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")



    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def delete(self, roomtype_mapping_id):
        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.valid_complete:
            mapping = RoomTypeMapping.revert_to_firstvalid(self.db, roomtype_mapping_id)
            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")
