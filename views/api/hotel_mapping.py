# -*- coding: utf-8 -*-

import traceback
from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.hotel import HotelModel
from models.hotel_mapping import HotelMappingModel
from models.room_type_mapping import RoomTypeMappingModel
from models.room_type import RoomTypeModel

from exception.json_exception import JsonException

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from tools.log import Log
from constants import PERMISSIONS

class HotelMappingAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid, json=True)
    def put(self):
        req = ObjectDict(json_decode(self.request.body))
        Log.info("HotelMapping>> user:{} req:{}".format(self.current_user, req))
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
        args = self.get_json_arguments()
        chain_hotel_id, main_hotel_id, merchant_id, merchant_name = get_and_valid_arguments(args,
                'chain_hotel_id', 'main_hotel_id', 'merchant_id', 'merchant_name')
        hotel = HotelModel.get_by_id(self.db, main_hotel_id)

        hotel_mapping = HotelMappingModel.get_by_provider_and_main_hotel(self.db, 6, chain_hotel_id, main_hotel_id)
        if hotel_mapping:
            raise JsonException(errcode=1000, errmsg="already exist")

        hotel_mapping = HotelMappingModel.new_hotel_mapping_from_ebooking(self.db,
                chain_hotel_id, hotel.name, hotel.address, hotel.city_id, main_hotel_id, merchant_id, merchant_name)

        self.finish_json(result=dict(
            hotel_mapping=hotel_mapping.todict(),
            ))

class HotelMappingEbookingBatchPushAPIHandler(BtwBaseHandler):

    def post(self):
        Log.info("start push ebooking hotel")
        print self.request.body
        args = self.get_json_arguments()

        hotels, = get_and_valid_arguments(args, 'hotels')
        hotel_mappings = self.add_hotels(hotels)

        Log.info("end push ebooking hotel")
        self.finish_json(result=dict(
            hotel_mapping=[hotel_mapping.todict() for hotel_mapping in hotel_mappings],
            ))

    def add_hotels(self, hotels):
        hotel_mappings = []
        for hotel in hotels:
            try:
                hotel_mapping = self.add_hotel_mapping(hotel)
                hotel_mappings.append(hotel_mapping)
            except:
                Log.info(">>> push ebooking hotel {} fail !!!".format(hotel))
                Log.error(traceback.format_exc())
                self.db.rollback()
        return hotel_mappings

    def add_hotel_mapping(self, hotel):
        Log.info(">>> push ebooking hotel {}".format(hotel))
        hotel_mapping = HotelMappingModel.get_by_provider_hotel(self.db, 6, hotel['chain_hotel_id'])
        main_hotel = HotelModel.get_by_id(self.db, hotel['main_hotel_id'])

        if hotel_mapping:
            Log.info(">>> modify exist ebooking hotel {}".format(hotel))
            hotel_mapping.merchant_id = hotel['merchant_id']
            hotel_mapping.merchant_name = hotel['merchant_name']
            hotel_mapping.info = 'update by ebooking'
            hotel_mapping.status = hotel_mapping.STATUS.valid_complete
            hotel_mapping.city_id = main_hotel.city_id
            hotel_mapping.provider_hotel_name = main_hotel.name
            hotel_mapping.provider_hotel_address = main_hotel.address
            hotel_mapping.main_hotel_id = main_hotel.id
            self.db.commit()
        else:
            Log.info(">>> new exist ebooking hotel {}".format(hotel))
            hotel_mapping = HotelMappingModel.new_hotel_mapping_from_ebooking(self.db,
                hotel['chain_hotel_id'], main_hotel.name, main_hotel.address, main_hotel.city_id, hotel['main_hotel_id'], hotel['merchant_id'], hotel['merchant_name'])

        return hotel_mapping

