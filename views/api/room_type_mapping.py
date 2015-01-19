# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.room_type import RoomTypeModel
from models.room_type_mapping import RoomTypeMappingModel

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from constants import PERMISSIONS
from exception.json_exception import JsonException

class RoomTypeMappingAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))

        r = RoomTypeMappingModel.update_main_hotel_id(self.db, req.id, req.main_roomtype_id)

        self.finish_json(result=ObjectDict(
                roomtype_mapping=r.todict(),
            ))



class RoomTypeMappingEbookingPushAPIHandler(BtwBaseHandler):

    def post(self):
        args = self.get_json_arguments()
        chain_hotel_id, chain_roomtype_id, main_roomtype_id = get_and_valid_arguments(args,
                'chain_hotel_id', 'chain_roomtype_id', 'main_roomtype_id')
        roomtype = RoomTypeModel.get_by_id(self.db, main_roomtype_id)

        roomtype_mapping = RoomTypeMappingModel.get_by_provider_and_main_roomtype(self.db, chain_roomtype_id, main_roomtype_id)
        if roomtype_mapping:
            raise JsonException(errcode=1000, errmsg="already exist")

        roomtype_mapping = RoomTypeMappingModel.new_roomtype_mapping_from_ebooking(self.db, chain_hotel_id, chain_roomtype_id, roomtype.name, roomtype.hotel_id, main_roomtype_id)

        self.finish_json(result=dict(
            roomtype_mapping=roomtype_mapping.todict()
            ))





