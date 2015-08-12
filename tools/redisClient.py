# -*- coding: utf-8 -*-
__author__ = 'jiangfuqiang'

import redis
from config import POI_REDIS_HOST

def connectRedis():
    r = redis.Redis(host=POI_REDIS_HOST,port=6379)
    return r

def put(key,value):
    r = connectRedis()
    r.lpush(key, value)