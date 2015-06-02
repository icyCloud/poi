# -*- coding: utf-8 -*-

import time

from tornado.escape import json_decode

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from tools.log import Log, log_request
from tools.request_tools import get_and_valid_arguments

from models.hotel import HotelModel as Hotel
from models.room_type import RoomTypeModel
from models.business_zone import BusinessZoneModel
from models.city import CityModel

from constants import EBOOKING_CHAIN_ID

class HotelSearchAPIHandler(BtwBaseHandler):

    @log_request
    def get(self):
        name = self.get_query_argument('name', None)
        star = self.get_query_argument('star', None)
        city_id = self.get_query_argument('city_id', None)
        district_id = self.get_query_argument('district_id', None)
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 10)
        filter_ids = self.get_query_argument('filter_ids', None)
        filter_ids = json_decode(filter_ids) if filter_ids else filter_ids
        within_ids = self.get_query_argument('within_ids', None)
        within_ids = json_decode(within_ids) if within_ids else within_ids
        count_total = True if int(self.get_query_argument('count_total', 0)) == 1 else False
        with_roomtype = int(self.get_query_argument('with_roomtype', 0))

        if count_total:
            hotels, total = Hotel.query(self.db, name, star, city_id, district_id, start, limit, filter_ids, within_ids, count_total=count_total)
        else:
            hotels = Hotel.query(self.db, name, star, city_id, district_id, start, limit, filter_ids, within_ids, count_total=count_total)
            total = 20000

        hotels = [hotel.todict() for hotel in hotels]

        self.merge_business_zone(hotels)
        self.merge_city(hotels)
        if with_roomtype == 1:
            self.merge_roomtype(hotels)

        self.finish_json(result=dict(
                hotels=hotels,
                start=start,
                limit=limit,
                total=total,
            ))

    def merge_business_zone(self, hotels):
        business_zone_ids = [hotel['business_zone'] for hotel in hotels]
        business_zones = BusinessZoneModel.get_by_ids(self.db, business_zone_ids)
        for hotel in hotels:
            for business_zone in business_zones:
                if business_zone.id == hotel['business_zone']:
                    hotel['business_zone'] = business_zone.todict()
                    break
        return hotels

    def merge_roomtype(self, hotels):
        hotel_ids = [h.id for h in hotels]
        rooms = RoomTypeModel.gets_by_hotel_ids(self.db, hotel_ids)
        for hotel in hotels:
            hotel['roomtypes'] = [room.todict() for room in rooms if room.hotel_id == hotel.id]
        return hotels

    def merge_city(self, hotels):
        city_ids = [h['city_id'] for h in hotels]
        citys = [city.todict() for city in CityModel.get_by_ids(self.db, city_ids)]
        for hotel in hotels:
            for city in citys:
                if hotel['city_id'] == city['id']:
                    hotel['city'] = city
                    break
        return hotels





class HotelAPIHandler(BtwBaseHandler):

    def get(self, hotel_id):
        hotel = Hotel.get_by_id(self.db, hotel_id)
        if hotel:
            self.finish_json(result={
                'hotel': hotel.todict()})
        else:
            self.finish_json(errcode=404, errmsg="not found hotel " + hotel_id)

    def post(self):
        args = self.get_json_arguments()
        name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, business_zone, phone, traffic, description, require_idcard, is_online, foreigner_checkin = get_and_valid_arguments(
                args,
                'name', 'star', 'facilities', 'blog', 'blat', 'glog', 'glat', 'city_id', 'district_id', 'address',
                'business_zone', 'phone', 'traffic', 'description', 'require_idcard', 'is_online', 'foreigner_checkin')
        hotel = Hotel.new(self.db,
            name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, business_zone, phone, traffic, description, require_idcard, is_online, foreigner_checkin)

        self.finish_json(result=dict(
            hotel=hotel.todict(),
            ))


    def put(self, hotel_id):
        args = self.get_json_arguments()
        name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, business_zone, phone, traffic, description, require_idcard, is_online, foreigner_checkin = get_and_valid_arguments(
                args,
                'name', 'star', 'facilities', 'blog', 'blat', 'glog', 'glat', 'city_id', 'district_id', 'address',
                'business_zone', 'phone', 'traffic', 'description', 'require_idcard', 'is_online', 'foreigner_checkin')

        hotel = Hotel.get_by_id(self.db, hotel_id)
        if not hotel:
            self.finish_json(errcode=404, errmsg="not found hotel " + hotel_id)
            return

        hotel = Hotel.update(self.db, hotel_id,
            name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, business_zone, phone, traffic, description, require_idcard, is_online, foreigner_checkin)

        self.finish_json(result=dict(
            hotel=hotel.todict(),
            ))
