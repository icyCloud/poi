# -*- coding: utf-8 -*-


from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from models.room_type import RoomTypeModel as RoomType
from models.hotel import HotelModel as Hotel
from models.facility import FacilityModel
from models.hotel_mapping import HotelMappingModel as HotelMapping
from models.poi_operate_log_mapping import PoiOperateLogModel as PoiOperateLogMapping
from config import modules
from config import motivations
from config import roomtypes
from mixin.roomtype_valid_mixin import RoomTypeValidMixin
from tools.log import Log, log_request
import traceback

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

        try:
            module = modules['first_valid']
            motivation = motivations['add_roomtype']
            operator = self.current_user
            poi_hotel_id =hotel.id
            poi_roomtype_id = _roomtype.id
            otaId = -1
            hotel_id = "-1"
            hotelModel = Hotel.get_by_id(self.db,poi_hotel_id)
            hotelName = hotelModel.name
            roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
            operate_content = u"新增"+_roomtype.name+"," + roomtypes[_roomtype.bed_type]+"," + str(_roomtype.floor) + u"楼"

            PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                            poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
        except Exception,e:
            traceback.print_exc()
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
        tempRoomType = RoomType.get_by_id(self.db,roomtype['id'])
        tempName = tempRoomType.name
        tempBedType = tempRoomType.bed_type
        tempFloor = tempRoomType.floor
        tempArea = tempRoomType.area
        _roomtype = RoomType.update(self.db, **roomtype)
        try:
            module = modules['first_valid']
            motivation = motivations['modify_roomtype']
            operator = self.current_user
            poi_hotel_id =hotel.id
            poi_roomtype_id = _roomtype.id
            otaId = -1
            hotel_id = "-1"
            hotelModel = Hotel.get_by_id(self.db,poi_hotel_id)
            hotelName = hotelModel.name
            roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
            operate_content = ''
            if tempName != _roomtype.name:
                operate_content += u'将' + tempName + u"修改为" + _roomtype.name + ","
            if tempBedType != _roomtype.bed_type:
                operate_content += u'将' + roomtypes[tempBedType] + u'修改为' + roomtypes[_roomtype.bed_type] + ","
            if tempFloor != _roomtype.floor:
                operate_content += u'将' + str(tempFloor) + "楼修改为" + str(_roomtype.floor) + "楼,"
            if tempArea != _roomtype.area:
                operate_content += u'将' + str(tempArea) + "平米修改为" + str(_roomtype.area) + "平米,"

            PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                            poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
        except Exception,e:
            traceback.print_exc()
        return self.finish_json(result=ObjectDict(
            roomtype=_roomtype.todict(),
            ))

    def merge_facility(self, roomtypes):
        facilities = FacilityModel.get_all_type_is_room(self.db)
        for roomtype in roomtypes:
            fas = roomtype.facility.split('|')
            _facilities = [facility.name for facility in facilities if str(facility.id) in fas]
            roomtype.facility = '|'.join(_facilities)


class RoomTypeInnerAPIHandler(BtwBaseHandler, RoomTypeValidMixin):

    def post(self, hotel_id):
        roomtype = ObjectDict(json_decode(self.request.body))
        if not self.valid_roomtype(roomtype):
            return self.finish_json(errcode=401, errmsg="无效的参数")

        hotel = Hotel.get_by_id(self.db, hotel_id)

        if not hotel:
            return self.finish_json(errcode=404, errmsg="无效的Hotel")

        _roomtype = RoomType.new(self.db, hotel_id, **roomtype)

        try:
            module = modules['first_valid']
            motivation = motivations['add_roomtype']
            operator = '程序自动匹配'
            poi_hotel_id =hotel.id
            poi_roomtype_id = _roomtype.id
            otaId = -1
            hotel_id = "-1"
            hotelModel = Hotel.get_by_id(self.db,poi_hotel_id)
            hotelName = hotelModel.name
            roomType = RoomType.get_by_id(self.db,id=poi_roomtype_id)
            operate_content = u"新增"+_roomtype.name+"," + roomtypes[_roomtype.bed_type]+"," + str(_roomtype.floor) + u"楼"

            PoiOperateLogMapping.record_log(self.db,otaId=otaId,hotelName=hotelName,module=module,motivation=motivation,operator=operator,
                                            poi_hotel_id=poi_hotel_id,operate_content=operate_content,hotel_id=hotel_id,poi_roomtype_id=poi_roomtype_id)
        except Exception,e:
            traceback.print_exc()
        return self.finish_json(result=ObjectDict(
            roomtype=_roomtype.todict(),
            ))