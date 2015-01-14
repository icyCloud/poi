# -*- coding: utf-8 -*-

from tools.log import Log
from models.stock.room_type import RoomTypeModel


class HotelMixin(object):

    def add_provider_roomtype(self, hotels):
        roomtypes = self.fetch_provider_hotel_room_types(hotels)
        if roomtypes:
            self.merge_provider_roomtypes(hotels, roomtypes)

    def fetch_provider_hotel_room_types(self, hotels):
        session = self.application.DB_Session_stock()
        hotel_ids = [hotel.provider_hotel_id for hotel in hotels]
        roomtypes = RoomTypeModel.gets_by_hotel_ids(session, hotel_ids)
        roomtypes = [roomtype.todict() for roomtype in roomtypes]
        session.close()
        #Log.info(">>>> roomtypes: {}".format(roomtypes))
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


