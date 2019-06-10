#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

class DB(object):
    """
    Database object
    Store data of each md step
    """
    def __init__(self,name):
        self.db_file = name+"_db"

        self.s_t = None
        self.s_tdot = None
        self.p_t = None
        self.v_t = None
        self.h_t = None
        self.h_tdot = None
        self.x_t = None
        self.x_tdot = None
        self.f_t = None
