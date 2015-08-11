# -*- coding: utf-8 -*-
__author__ = 'jiangfuqiang'
from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class PoiOperateLogHandler(BtwBaseHandler):
    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.POI)
    def get(self):
        self.render('poi_operate_log.html',nav=NAVIGATION.OPERATELOG)