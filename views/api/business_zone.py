# -*- coding: utf-8 -*-

from tornado.escape import json_decode

from views.base import BtwBaseHandler
from models.business_zone import BusinessZoneModel

class BusinessZoneByCityAPIHandler(BtwBaseHandler):

    def get(self, city_id):
        business_zones = BusinessZoneModel.get_by_city_id(self.db, city_id)

        self.finish_json(result=dict(
            business_zones = [b.todict() for b in business_zones],
            ))
