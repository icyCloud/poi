# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class PolymerHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.polymer)
    def get(self):
        self.render('polymer.html', nav=NAVIGATION.POLYMER)
