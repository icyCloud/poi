# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.room_type_mapping import RoomTypeMappingModel

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS

class RoomTypeMappingAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))

        r = RoomTypeMappingModel.update_main_hotel_id(self.db, req.id, req.main_roomtype_id)

        self.finish_json(result=ObjectDict(
                roomtype_mapping=r.todict(),
            ))







