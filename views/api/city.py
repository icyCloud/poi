# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler
from models.city import CityModel as City

class CityAPIHandler(BtwBaseHandler):

    def get(self):
        citys = City.get_all_dicts(self.db)
        self.set_header("Cache-Control", "max-age=3600, must-revalidate")
        self.finish_json(result=dict(
                citys=citys,
            ))
