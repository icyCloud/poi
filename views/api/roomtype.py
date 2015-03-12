# -*- coding: utf-8 -*-


from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from models.room_type import RoomTypeModel as RoomType
from models.hotel import HotelModel as Hotel
from models.facility import FacilityModel

from mixin.roomtype_valid_mixin import RoomTypeValidMixin
from tools.log import Log, log_request

class RoomTypeAPIHandler(BtwBaseHandler, RoomTypeValidMixin):

    @log_request
    def get(self, hotel_id):
        need_valid = self.get_query_argument('need_valid', 1)
        need_valid = True if need_valid == 1 else False
        hotel = Hotel.get_by_id(self.db, hotel_id)
        if hotel:
            hotel = hotel.todict()
            rooms = RoomType.gets_by_hotel_id(self.db, hotel_id, need_valid=need_valid)
            rooms = [room.todict() for room in rooms]

            Log.info(u"fetch rooms {}".format(rooms))

            return self.finish_json(result=dict(
                    roomtypes=rooms,
                    hotel=hotel,
                ))
        else:
            return self.finish_json(errcode=404, errmsg="无效的Hotel")

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.POI)
    def post(self, hotel_id):
        roomtype = ObjectDict(json_decode(self.request.body))
        if not self.valid_roomtype(roomtype):
            return self.finish_json(errcode=401, errmsg="无效的参数")

        hotel = Hotel.get_by_id(self.db, hotel_id)

        if not hotel:
            return self.finish_json(errcode=404, errmsg="无效的Hotel")

        _roomtype = RoomType.new(self.db, hotel_id, **roomtype)

        return self.finish_json(result=ObjectDict(
            roomtype=_roomtype.todict(),
            ))

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.POI)
    def put(self, hotel_id):
        roomtype = ObjectDict(json_decode(self.request.body))
        if not self.valid_roomtype(roomtype):
            return self.finish_json(errcode=401, errmsg="无效的参数")

        hotel = Hotel.get_by_id(self.db, hotel_id)

        if not hotel:
            return self.finish_json(errcode=404, errmsg="无效的Hotel")

        _roomtype = RoomType.update(self.db, **roomtype)

        return self.finish_json(result=ObjectDict(
            roomtype=_roomtype.todict(),
            ))

    def merge_facility(self, roomtypes):
        facilities = FacilityModel.get_all_type_is_room(self.db)
        for roomtype in roomtypes:
            fas = roomtype.facility.split('|')
            _facilities = [facility.name for facility in facilities if str(facility.id) in fas]
            roomtype.facility = '|'.join(_facilities)

        

