#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

class Structure:
    """
    Structure class
    """
    def __init__(self):
        self.lattice = None
        self.xred = None
        self.xcart = None
        self.fcart = None
        self.strten = None
        self.vel = None
        self.vel_h = None
        self.amu = None

    def get_lattice(self):
        return self.lattice

    def get_xred(self):
        return self.xred

    def get_xcart(self):
        return self.xcart

    def get_fcart(self):
        return self.fcart

    def get_strten(self):
        return self.strten

    def get_vel(self):
        return self.vel

    def get_vel_h(self):
        return self.vel_h

    def get_amu(self):
        return self.amu

    def set_lattice(self,lattice):
        return self.lattice = lattice

    def set_xred(self,xred):
        self.xred = xred

    def set_xcart(self,xcart):
        self.xcart = xcart

    def set_fcart(self,fcart):
        self.fcart = fcart

    def set_strten(self,strten):
        self.strten = strten

    def set_vel(self,vel):
        self.vel = vel

    def set_vel_h(self,vel_h):
        self.vel_h = vel_h

    def set_amu(self,amu):
        self.amu = amu
