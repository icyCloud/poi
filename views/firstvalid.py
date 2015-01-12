# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class FirstValidHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.first_valid)
    def get(self):
        self.render('firstvalid.html', nav=NAVIGATION.FIRSTVALID)

