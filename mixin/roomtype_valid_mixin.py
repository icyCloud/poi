# -*- coding: utf-8 -*-


from tools.valid import valid_dict_keys

class RoomTypeValidMixin(object):

    def valid_roomtype(self, roomtype):
        return valid_dict_keys(roomtype, u'name')
