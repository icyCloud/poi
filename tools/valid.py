# -*- coding: utf-8 -*-

def valid_dict_keys(_dict, *keys):
    for key in keys:
        if key not in _dict:
            return False
    return True
