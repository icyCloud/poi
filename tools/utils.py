# -*- coding: utf-8 -*-

import time

def exe_time(func):
    def _(*args, **args2):
            t0 = time.time()
            print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
            back = func(*args, **args2)
            print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
            print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
            return back
    return _

