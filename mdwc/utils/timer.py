#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

from datetime import timedelta
from time import time,strftime

def timer(function):
    """
    Decorator for timing a function call
    """
    def method(*args, **kwargs):
        start = time()
        rslt = function(*args, **kwargs)
        print '[%s] Elapsed time: %s' % (function.__name__,
                                         timedelta(time()-start))
        return rslt
    return method

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def today():
    return strftime("%d/%m/%Y %H:%M:%S")

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def today_txt():
    return strftime("%H:%M:%S %B %d, %Y")
