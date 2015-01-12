# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS, NAVIGATION

class RoomTypeHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.POI)
    def get(self, hotel_id):
        self.render('roomtype.html', nav=NAVIGATION.ROOMTYPE, hotel_id=hotel_id)

