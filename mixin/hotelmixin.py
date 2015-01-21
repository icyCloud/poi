# -*- coding: utf-8 -*-

import time

from tools.log import Log
from models.stock.room_type import RoomTypeModel


class HotelMixin(object):

    def add_provider_roomtype(self, hotels):
        roomtypes = self.fetch_provider_hotel_room_types(hotels)
        if roomtypes:
            self.merge_provider_roomtypes(hotels, roomtypes)

    def fetch_provider_hotel_room_types(self, hotels):
        roomtypes = [roomtype.todict() for roomtype in self.read_roomtypes(hotels)]
        return roomtypes


    def read_roomtypes(self, hotels):
        t0 = time.time()
        Log.info(">> get provider hotel")
        chains = {}
        for hotel in hotels:
            if hotel.provider_id in chains:
                chains[hotel.provider_id].append(hotel)
            else:
                chains[hotel.provider_id] = [hotel]

        roomtypes = []
        for provider_id in chains:
            hotel_ids = [hotel.id for hotel in chains[provider_id]]
            print provider_id, hotel_ids
            roomtypes.extend(RoomTypeModel.gets_by_chain_and_hotel_ids(self.db_stock, provider_id, hotel_ids))

        t1 = time.time()
        Log.info(">> get provider hotel cost {}".format(t1 - t0))

        return roomtypes

    def merge_provider_roomtypes(self, hotels, roomtypes):
        for hotel in hotels:
            for roomtype_mapping in hotel.roomtype_mappings:
                for roomtype in roomtypes:
                    if roomtype_mapping.provider_roomtype_id == roomtype['roomtype_id'] and roomtype_mapping.provider_id == roomtype['chain_id']:
                        roomtype_mapping['provider_roomtype'] = roomtype
                        roomtype_mapping['provider_roomtype']['area'] = roomtype.get('room_size', 0)
                        roomtype_mapping['provider_roomtype']['description'] = roomtype.get('desc', '')
                        roomtype_mapping['provider_roomtype']['capacity'] = roomtype.get('occupancy', '')
                        roomtype_mapping['provider_roomtype_name'] = roomtype.get('name')
                        break


