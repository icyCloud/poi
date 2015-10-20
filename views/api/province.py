# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from models.province import ProvinceModel as Province


class ProvinceAPIHandler(BtwBaseHandler):
    def get(self):
        provinces = Province.get_all_dicts(self.db)
        self.set_header("Cache-Control", "max-age=3600, must-revalidate")
        self.finish_json(result=dict(
            provinces=provinces
        ))
