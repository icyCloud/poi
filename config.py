# -*- coding: utf-8 -*-

Config = {
    'db' : 'mysql://btw:btw123@114.215.87.177:3306/devine_poi?charset=utf8',
    'db_stock': 'mysql://btw:btw123@114.215.87.177:3306/devine_stock2?charset=utf8',
}

LISTEN_IP = '0.0.0.0'

API = {
        'EBOOKING': 'http://127.0.0.1:9501',
        'STOCK': "http://114.215.87.61:8080",
        'ELONG': "http://10.168.245.187:8080",
}

IS_PUSH_TO_STOCK = False

REDIS_HOST = 'localhost'

BACKSTAGE_HOST = 'http://121.42.8.247:8080'
BACKSTAGE_USERNAME_KEY = "test_op_username"

DEBUG = True

COOKIE_SALT = 'TY30Rbs0k83ZAOSjApGlsNBlJ33kmNik'

BACKSTAGE_PERMISSION = {
        'admin': 55,
        'polymer': 56,
        'provider': 57,
        'first_valid': 58,
        'second_valid': 60,
        'price_rule': 61,
        'poi': 62,
        }

modules = {
      'first_valid':1,
      'second_valid':2,
      'merge':3,
      'poi_manage':4
}

showModeuls = {
    1:'初审',
    2:'终审',
    3:'聚合',
    4:'酒店管理'
}

motivations = {
        'pass_hotel':1,   #通过酒店
        'pass_roomtype':2,   #通过房型
        'modify_roomtype':3,   #修改房型
        'add_roomtype':4,   #添加房型
        'back_hotel':5,    #打回酒店
        'back_roomtype':6,    #打回房型
        'online_hotel':7,    #上线酒店
        'online_roomtype':8,    #上线房型
        'offline_hotel':9,   #下线酒店
        'offline_roomtype':10, #下线房型
        'add_hotel':11,    #新增酒店
        'new_roomtype':12    #新增房型

}

showMotivations = {
    1:'通过酒店',
    2:'通过房型',
    3:'修改房型',
    4:'添加房型',
    5:'打回酒店',
    6:'打回房型',
    7:'上线酒店',
    8:'上线房型',
    9:'下线酒店',
    10:'下线房型',
    11:'新增酒店',
    12:'新增房型'
}

roomtypes = {
    0:u"单床",
	1: u"大床",
	2:u"双床",
	3:u"三床",
	4:u"三床-1大2单",
	5:u"榻榻米",
	6:u"拼床",
	7:u"水床",
	8:u"榻榻米双床",
	9:u"榻榻米单床",
	10: u"圆床",
	11:u"上下铺",
	12:u"大床或双床",
	-1:u"未知"
}
