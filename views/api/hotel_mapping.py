# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.hotel_mapping import HotelMappingModel
from models.room_type_mapping import RoomTypeMappingModel
from models.room_type import RoomTypeModel

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS

class HotelMappingAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        mapping = HotelMappingModel.change_main_hotel_id(self.db, req.hotel_mapping_id, req.main_hotel_id)
        RoomTypeMappingModel.reset_mapping_by_provider_hotel_id(self.db, mapping.provider_hotel_id, req.main_hotel_id)
        room_types = RoomTypeModel.gets_by_hotel_id(self.db, req.main_hotel_id)
        room_types = [room_type.todict() for room_type in room_types]


        self.finish_json(result=dict(
            hotel_mapping=mapping.todict(),
            room_types=room_types,
            ))


class HotelMappingEbookingPushAPIHandler(BtwBaseHandler):

    def post(self):
        pass


