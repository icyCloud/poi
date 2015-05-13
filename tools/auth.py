# -*- coding: utf-8 -*-

from constants import PERMISSIONS
from config import BACKSTAGE_PERMISSION


def auth_login(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.current_user:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=100, errmsg="need login")
                else:
                    self.redirect(self.get_login_url())
        return _
    return _decorator


def auth_permission(permissions, json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.current_user_permission & permissions:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=401, errmsg="permission denied")
                else:
                    self.finish('permission denied')
        return _
    return _decorator

def mapping_permission(permissions):

    permission = 0
    if BACKSTAGE_PERMISSION['admin'] in permissions:
        permission = permission | PERMISSIONS.admin
    if BACKSTAGE_PERMISSION['polymer'] in permissions:
        permission = permission | PERMISSIONS.polymer
    if BACKSTAGE_PERMISSION['provider'] in permissions:
        permission = permission | PERMISSIONS.provider_list
    if BACKSTAGE_PERMISSION['first_valid'] in permissions:
        permission = permission | PERMISSIONS.first_valid
    if BACKSTAGE_PERMISSION['second_valid'] in permissions:
        permission = permission | PERMISSIONS.second_valid
    if BACKSTAGE_PERMISSION['price_rule'] in permissions:
        permission = permission | PERMISSIONS.price_rule
    if BACKSTAGE_PERMISSION['poi'] in permissions:
        permission = permission | PERMISSIONS.POI
    return permission
