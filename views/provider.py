# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class ProviderHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.provider_list)
    def get(self):
        self.render('provider.html', nav=NAVIGATION.PROVIDER)

