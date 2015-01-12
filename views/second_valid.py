# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class SecondValidHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.second_valid)
    def get(self):
        self.render('secondvalid.html', nav=NAVIGATION.SECONDVALID)

