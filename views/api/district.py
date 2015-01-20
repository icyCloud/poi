
# -*- coding: utf-8 -*-

from tornado.escape import json_decode

from views.base import BtwBaseHandler

from models.district import DistrictModel as District

class DistrictAPIHandler(BtwBaseHandler):

    def get(self):
        district_ids = self.get_query_argument('district_ids', None)
        district_ids = json_decode(district_ids) if district_ids else district_ids

        if district_ids:
            districts = District.get_by_ids(self.db, district_ids)
            districts = [district.todict() for district in districts]
        else:
            districts = District.get_all_dicts(self.db)

        self.finish_json(result=dict(
            districts=districts
            ))
