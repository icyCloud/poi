# -*- coding: utf-8 -*-

import logging

Log = logging.getLogger()
Log.setLevel(logging.INFO)

def log_request(fn):
    def _(self, *args, **kwargs):
        Log.info(self.request)
        return fn(self, *args, **kwargs)
    return _
