# -*- coding: utf-8 -*-

import time

from dogpile.cache import make_region 
from dogpile.cache.api import NO_VALUE

from constants import MC_PREFIX

region = make_region().configure(
        'dogpile.cache.redis',
        expiration_time=3600,
        arguments = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'redis_expiration_time': 60*60*2,   # 2 hours
        'distributed_lock': True
        }
        #arguments={
            #'url':["127.0.0.1"],
            #'binary':True,
            #'behaviors':{"tcp_nodelay": True,"ketama":True},
            #}
        )

def join_keys(*args):
    return '_'.join([str(arg) for arg in args])

def mc(key):
    def wrap(fn):
        def _(*args, **kwargs):
            t0 = time.time()
            mc_key = join_keys(MC_PREFIX, key)
            r = region.get(mc_key)
            t1 = time.time()
            print '=' * 20
            print t1-t0
            if r is NO_VALUE:
                r = fn(*args, **kwargs)
                region.set(mc_key, r)
                return r
            else:
                return r
        return _
    return wrap

def mc_with_id(key):
    def wrap(fn):
        def _(inst, session, id, *args, **kwargs):
            mc_key = join_keys(MC_PREFIX, key, id)
            r = region.get(mc_key)
            if r is NO_VALUE:
                r = fn(inst, session, id, *args, **kwargs)
                region.set(mc_key, r)
                return r
            else:
                return r
        return _
    return wrap


def set(key, value):
    mc_key = join_keys(MC_PREFIX, key)
    return region.set(mc_key, value)

def delete(key):
    mc_key = join_keys(MC_PREFIX, key)
    return region.delete(mc_key)

def get(key, expiration_time=None, ignore_expiration=False):
    mc_key = join_keys(MC_PREFIX, key)
    return region.get(mc_key, expiration_time, ignore_expiration)

def get_or_create(key, creator, expiration_time=None, should_cache_fn=None):
    mc_key = join_keys(MC_PREFIX, key)
    return region.get_or_create(mc_key, creator, expiration_time=None, should_cache_fn=None)


