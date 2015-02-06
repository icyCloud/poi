# -*- coding: utf-8 -*-

Config = {
    'db' : 'mysql://root:root@192.168.10.15:3306/devine_poi?charset=utf8',
    'db_stock': 'mysql://btw:btw123@114.215.87.177:3306/devine_stock2?charset=utf8',
}

LISTEN_IP = '0.0.0.0'

API = {
        'EBOOKING': 'http://127.0.0.1:9501',
        'STOCK': "http://114.215.87.61:8080",
}

IS_PUSH_TO_STOCK = False

REDIS_HOST = 'localhost'
