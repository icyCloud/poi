# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

# Permissions
PERMISSIONS = ObjectDict({

        'admin':                0b00000000000000001,
        'polymer':              0b00000000000000010,
        'provider_list':        0b00000000000000100,
        'first_valid':          0b00000000000001000,
        'second_valid':         0b00000000000010000,
        'price_rule':           0b00000000000100000,
        'POI':                  0b00000000001000000,
        })

#Navigation
NAVIGATION = ObjectDict(
    USERMANAGER=0,
    PROVIDER=1,
    FIRSTVALID=2,
    SECONDVALID=3,
    POLYMER=4,
    ROOMTYPE = 5,
    )

#Memcached
MC_PREFIX = "poi_mc"

EBOOKING_CHAIN_ID = 6

class Login(object):
    from config import BACKSTAGE_HOST
    LOGIN_URL = BACKSTAGE_HOST + '/backstage/login'
    PERMISSION_URL = BACKSTAGE_HOST + '/backstage/app/order_query/list?username={}'
