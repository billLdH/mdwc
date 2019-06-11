#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

class Structure(DFT):
    """
    Structure Object updated after each md step
    """
    def __init__(self, filename, acell=None,xred, xcart=None,fcart=None,
                 strten=None, vel=None, vel_h=None, amu=None):

        # Time:t+dt
        self.s_tdot = None
        self.h_tdot = None
        self.x_tdot = None

        if filename is None:
            # Unchanged
            self.natom = natom
            self.ntypat = ntypat
            self.typat = typat
            self.xcart = xcart
            self.amu = amu

            # Time:t
            self.s_t = strten
            self.v_t = vel
            self.hv_t = vel_h
            self.h_t = lattice
            self.x_t = xred
            self.f_t = fcart
        else:
            read_structure(self.dft_code,filename)

    def get_dft_code(self):
        return self.dft_code

    def read_structure(self):
        struct= DFT.read_structure(filename)
        read_from_dict(struct)

    def read_from_dict(self,dict):
        self.natom= dict["natom"]
        self.ntypat= dict["ntypat"]
        self.typat= dict["typat"]
        self.amu= dict["amu"]
        self.s_t= dict["strten"]
        self.v_t= dict["vel"]
        self.hv_t= dict["vel_h"]
        self.h_t= dict["lattice"]
        self.x_t=dict["xred"]
        self.f_t= dict["fcart"]

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
