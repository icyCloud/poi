# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler
from models.city import CityModel as City

class CityAPIHandler(BtwBaseHandler):

    def get(self):
        citys = [city.todict() for city in City.get_all(self.db)]
        self.finish_json(result=dict(
                citys=citys,
            ))
