# -*- coding: utf-8 -*-

import time

from tornado.util import ObjectDict
from tornado import gen
from tornado.escape import json_encode, json_decode

from views.base import BtwBaseHandler, StockHandler
from mixin.hotelmixin import HotelMixin
from mixin.stockmixin import StockMixin

from tools.auth import auth_login, auth_permission
from tools.log import Log, log_request
from constants import PERMISSIONS
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.hotel import HotelModel as Hotel
from models.room_type_mapping import RoomTypeMappingModel as RoomTypeMapping
from models.poi_operate_log_mapping import PoiOperateLogModel as PoiOperateLogMapping
from models.room_type import RoomTypeModel as RoomType
from models.city import CityModel
from models.district import DistrictModel
from config import modules
from config import motivations
from tools import redisClient
import traceback
from tools import log
import datetime


class PolymerAPIHandler(StockHandler, HotelMixin):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    @log_request
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)

        provider_id = self.get_query_argument('provider_id', None)
        hotel_name = self.get_query_argument('hotel_name', None)
        city_id = self.get_query_argument('city_id', None)
        show_online_type = self.get_query_argument('show_online_type', 0)
        show_online_type = int(show_online_type)

        Log.info(">> get show in polymer")
        t0 = time.time() 
        hotel_mappings, total = HotelMapping.gets_show_in_polymer(self.db,
                provider_id=provider_id, hotel_name=hotel_name, city_id=city_id, show_online_type=show_online_type,
                start=start, limit=limit)
        t1 = time.time()
        Log.info(">> show in polymer cost {}".format(t1 - t0))

        hotels = [hotel.todict() for hotel in hotel_mappings]
        t2 = time.time()
        self.merge_main_hotel_info(hotels)
        t3 = time.time()
        Log.info(">> merge main hotel info cost {}".format(t3 - t2))

        t4 = time.time()
        self.merge_room_type_mapping(hotels)
        t5 = time.time()
        Log.info(">> merge roomtype mapping cost {}".format(t5 - t4))

        t6 = time.time()
        self.add_provider_roomtype(hotels)
        t7 = time.time()
        Log.info(">> add provider roomtype cost {}".format(t7 - t6))

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

        roomtype_mappings = RoomTypeMapping.get_polymer_provider_hotel_ids(self.db, provider_hotel_ids)
        roomtype_mappings = [mapping.todict() for mapping in roomtype_mappings]

        main_hotel_ids = [mapping.main_hotel_id for mapping in roomtype_mappings]
        main_hotel_ids = {}.fromkeys(main_hotel_ids).keys()
        main_hotel_ids.sort()

        self.roomtypes = RoomType.gets_by_hotel_ids(self.db, main_hotel_ids)
        self.roomtypes =[roomtype.todict() for roomtype in self.roomtypes]

        self.merge_room_type(self.roomtypes, roomtype_mappings)

        for hotel in hotel_dicts:
            roomtype_mapping_dicts = [
                roomtype_mapping
                for roomtype_mapping in roomtype_mappings
                if hotel.provider_id == roomtype_mapping.provider_id\
                        and hotel.provider_hotel_id == roomtype_mapping.provider_hotel_id]
            hotel['roomtype_mappings'] = roomtype_mapping_dicts
            
    def merge_room_type(self, roomtypes, room_type_mapping_dicts):
        for mapping in room_type_mapping_dicts:
            for roomtype in roomtypes:
                if mapping.main_roomtype_id == roomtype.id:
                    mapping['main_roomtype'] = roomtype


class PolymerHotelAPIHandler(BtwBaseHandler, StockMixin):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        Log.info("Polymer>>Hotel>>Online>> user:{} req:{}".format(self.current_user, req))
        hotel_mapping_id = req.hotel_mapping_id
        is_online = req.is_online


        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.valid_complete:
            hotel_mapping = HotelMapping.set_online(self.db, hotel_mapping_id, is_online)
            if hotel_mapping.is_online in [0, -1]:
                RoomTypeMapping.disable_by_provider_hotel_id(self.db, hotel_mapping.provider_hotel_id)

            try:
                redisClient.put('poi_online',hotel_mapping.main_hotel_id)
            except Exception,e:
                traceback.print_exc()
            yield self.notify_stock(hotel_mapping.provider_id, hotel_mapping.provider_hotel_id)
            try:
                module = modules['merge']
                motivation = None
                if is_online in [0, -1]:
                    motivation = motivations['offline_hotel']
                else:
                    motivation = motivations['online_hotel']
                operator = self.current_user
                poi_hotel_id = hotel_mapping.main_hotel_id
                otaId = hotel_mapping.provider_id
                hotelName = hotel_mapping.provider_hotel_name
                hotelModel = Hotel.get_by_id(self.db,id=poi_hotel_id)
                operate_content = hotelName + "<->" + hotelModel.name
                hotel_id = hotel_mapping_id
                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def delete(self, hotel_mapping_id):
        Log.info("Polymer>>Hotel {}>>Delete>> user:{}".format(hotel_mapping_id, self.current_user))
        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if hotel_mapping and hotel_mapping.status == hotel_mapping.STATUS.valid_complete:
            hotel_mapping = HotelMapping.revert_to_firstvalid(self.db, hotel_mapping_id)
            RoomTypeMapping.revert_to_firstvalid_by_provider_hotel_id(self.db, hotel_mapping.provider_hotel_id)

            try:
                module = modules['merge']
                motivation = motivations['back_hotel']
                operator = self.current_user
                poi_hotel_id = hotel_mapping.main_hotel_id
                otaId = hotel_mapping.provider_id
                hotelName = hotel_mapping.provider_hotel_name
                hotelModel = Hotel.get_by_id(self.db,id=poi_hotel_id)
                operate_content = hotelName + "<->" + hotelModel.name
                hotel_id = hotel_mapping_id
                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                hotel_mapping=hotel_mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")


class PolymerRoomTypeAPIHandler(BtwBaseHandler, StockMixin):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        Log.info("Polymer>>RoomTypeModel>>Online>> user:{} req:{}".format(self.current_user, req))
        roomtype_mapping_id = req.roomtype_mapping_id
        hotel_mapping_id = req.hotel_mapping_id
        is_online = req.is_online

        hotel_mapping = HotelMapping.get_by_id(self.db, hotel_mapping_id)
        if is_online == 1:
            if not hotel_mapping or hotel_mapping.is_online in [0, -1]:
                self.finish_json(errcode=402, errmsg="hotel mapping not online")
                return

        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.valid_complete:
            RoomTypeMapping.set_online(self.db, roomtype_mapping_id, is_online)
            try:
                redisClient.put('poi_online',mapping.main_hotel_id)
            except Exception,e:
                traceback.print_exc()
            yield self.notify_stock(hotel_mapping.provider_id, hotel_mapping.provider_hotel_id)
            try:
                module = modules['merge']
                motivation = None
                if is_online == 1:
                    motivation = motivations['online_roomtype']
                else:
                    motivation = motivations['offline_roomtype']
                operator = self.current_user
                poi_hotel_id = mapping.main_hotel_id
                poi_roomtype_id = mapping.main_roomtype_id
                otaId = mapping.provider_id
                hotel_id = mapping.provider_hotel_id
                hotelModel = HotelMapping.get_by_provider_and_main_hotel(self.db,otaId,hotel_id,poi_hotel_id)
                hotelName = hotelModel.provider_hotel_name
                roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
                operate_content = mapping.provider_roomtype_name + " <-> " + roomType.name

                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                                poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")



    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    def delete(self, roomtype_mapping_id):
        Log.info("Polymer>>RoomType {}>>Delete>> user:{}".format(roomtype_mapping_id, self.current_user))
        mapping = RoomTypeMapping.get_by_id(self.db, roomtype_mapping_id)
        if mapping and mapping.status == mapping.STATUS.valid_complete:
            mapping = RoomTypeMapping.revert_to_firstvalid(self.db, roomtype_mapping_id)

            try:
                module = modules['merge']
                motivation = motivations['back_roomtype']
                operator = self.current_user
                poi_hotel_id = mapping.main_hotel_id
                poi_roomtype_id = mapping.main_roomtype_id
                otaId = mapping.provider_id
                hotel_id = mapping.provider_hotel_id
                hotelModel = HotelMapping.get_by_provider_and_main_hotel(self.db,otaId,hotel_id,poi_hotel_id)
                hotelName = hotelModel.provider_hotel_name
                roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
                operate_content = mapping.provider_roomtype_name + " <-> " + roomType.name

                PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                                poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
            except Exception,e:
                traceback.print_exc()

            self.finish_json(result=ObjectDict(
                roomtype_mapping=mapping.todict(),
                ))
        else:
            self.finish_json(errcode=401, errmsg="not in second valid")

class PolymerHotelLineHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer, json=True)
    @log_request
    def put(self):
        jon = self.get_json_arguments()
        startTime = jon['startTime']
        endTime = jon['endTime']
        line = jon['line']
        chainIds = jon['chainIds']
        errcode = 0
        errmsg = 'success'
        try:
            if startTime and endTime and chainIds:
                HotelMapping.set_mult_line(self.db,chainIds=chainIds,startTime=startTime,endTime=endTime,is_online=int(line))
            else:
                errcode = 1
                errmsg = 'failure'
        except Exception,e:
            traceback.print_exc()
        finally:
            Log.info(self.current_user+'在'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "批量修改了"+chainIds+"的酒店状态为：" + str(line))
            self.finish_json(errcode=errcode, errmsg=errmsg)