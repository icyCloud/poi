# -*- coding: utf-8 -*-

from tornado.escape import json_decode

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from models.hotel import HotelModel as Hotel
from models.business_zone import BusinessZoneModel

class HotelSearchAPIHandler(BtwBaseHandler):

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


        hotels, total = Hotel.query(self.db, name, star, city_id, district_id, start, limit, filter_ids, within_ids)
        hotels = [hotel.todict() for hotel in hotels]

        self.merge_business_zone(hotels)
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




class HotelAPIHandler(BtwBaseHandler):

    def get(self, hotel_id):
        hotel = Hotel.get_by_id(self.db, hotel_id)
        if hotel:
            self.finish_json(result={
                'hotel': hotel.todict()})
        else:
            self.finish_json(errcode=404, errmsg="not found hotel " + hotel_id)

