# -*- coding: utf-8 -*-

import traceback

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.room_type import RoomTypeModel
from models.room_type_mapping import RoomTypeMappingModel

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from tools.log import Log
from constants import PERMISSIONS
from exception.json_exception import JsonException

class RoomTypeMappingAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        Log.info("RoomTypeMapping>> user:{}, req:{}".format(self.current_user, req))

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
        Log.info('args: ' + str(args))
        roomtype_mapping = RoomTypeMappingModel.get_by_provider_and_main_roomtype(self.db, 6, chain_roomtype_id, main_roomtype_id,chain_hotel_id,is_delete=-1)
        if roomtype_mapping:
            Log.info('exist roomtype mapping: ' + str(args))
            if roomtype_mapping.is_delete == 1:
                RoomTypeMappingModel.delete_mapping_by_provider_hotel_id(self.db,6,chain_hotel_id,chain_roomtype_id,is_delete=0)
            else:
                raise JsonException(errcode=1000, errmsg="already exist")
        else:
            roomtype_mapping = RoomTypeMappingModel.new_roomtype_mapping_from_ebooking(self.db, chain_hotel_id, chain_roomtype_id, roomtype.name, roomtype.hotel_id, main_roomtype_id)

        self.finish_json(result=dict(
            roomtype_mapping=roomtype_mapping.todict()
            ))


class RoomTypeMappingEbookingBatchPushAPIHandler(BtwBaseHandler):

    def post(self):
        args = self.get_json_arguments()

        roomtypes, = get_and_valid_arguments(args, 'roomtypes')

        roomtype_mappings = self.add_roomtypes(roomtypes)


        self.finish_json(result=dict(
            roomtype_mapping=[roomtype_mapping.todict() for roomtype_mapping in roomtype_mappings]
            ))

    def add_roomtypes(self, roomtypes):
        roomtype_mappings = []
        for roomtype in roomtypes:
            try:
                roomtype_mapping = self.add_roomtype(roomtype)
                roomtype_mappings.append(roomtype_mapping)
            except:
                Log.info(">>> push ebooking room {} fail !!!".format(roomtype))
                Log.error(traceback.format_exc())
                self.db.rollback()

        return roomtype_mappings 

    def add_roomtype(self, roomtype):
        Log.info(">>> push ebooking room {}".format(roomtype))
        roomtype_mapping = RoomTypeMappingModel.get_by_provider_roomtype(self.db, 6, roomtype['chain_roomtype_id'],roomtype['chain_hotel_id'])
        
        main_roomtype = RoomTypeModel.get_by_id(self.db, roomtype['main_roomtype_id'])

        if roomtype_mapping:
            Log.info(">>> modify exist ebooking room {}".format(roomtype))
            roomtype_mapping.provider_hotel_id = roomtype['chain_hotel_id'] 
            roomtype_mapping.provider_roomtype_name = main_roomtype.name
            roomtype_mapping.main_hotel_id = main_roomtype.hotel_id
            roomtype_mapping.main_roomtype_id = main_roomtype.id
            roomtype_mapping.status = roomtype_mapping.STATUS.valid_complete
            self.db.commit()
        else:
            Log.info(">>> new ebooking room {}".format(roomtype))
            roomtype_mapping = RoomTypeMappingModel.new_roomtype_mapping_from_ebooking(self.db,
                    roomtype['chain_hotel_id'],
                    roomtype['chain_roomtype_id'],
                    main_roomtype.name, main_roomtype.hotel_id,
                    roomtype['main_roomtype_id'])
        return roomtype_mapping

class RoomTypeMappingEbookingDeleteAPIHandler(BtwBaseHandler):

    def post(self):
        args = self.get_json_arguments()
        Log.info('args: ' + str(args))
        chain_hotel_id, chain_roomtype_id = get_and_valid_arguments(args,
                'chain_hotel_id', 'chain_roomtype_id')

        if chain_hotel_id and chain_roomtype_id:

            RoomTypeMappingModel.delete_mapping_by_provider_hotel_id(self.db,6, chain_hotel_id, chain_roomtype_id)

            self.finish_json()
        else:
            self.finish_json(errcode=1)




