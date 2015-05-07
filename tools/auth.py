# -*- coding: utf-8 -*-

from constants import PERMISSIONS


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
    if 55 in permissions:
        permission = permission | PERMISSIONS.admin
    if 56 in permissions:
        permission = permission | PERMISSIONS.polymer
    if 57 in permissions:
        permission = permission | PERMISSIONS.provider_list
    if 58 in permissions:
        permission = permission | PERMISSIONS.first_valid
    if 60 in permissions:
        permission = permission | PERMISSIONS.second_valid
    if 61 in permissions:
        permission = permission | PERMISSIONS.price_rule
    if 62 in permissions:
        permission = permission | PERMISSIONS.POI
    return permission
