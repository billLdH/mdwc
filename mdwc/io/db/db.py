#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

class DB(DBFormat):
    """
    Database object
    Store data of each md step
    In this db file, we could store for each step (few ideas):
      - MD info (Qmass, Bmass, dt, species, psp, natom,...) <= only once
      - Energy
          # DFT
          # Constraints' cost ?
      - Pressure
      - Temperature
      - Atomic positions (reduced and cartesian)
      - Cell (parameters and angles)
      - Volume
      - Stress tensor
      - Forces (atoms, cell,...)

    """
    def __init__(self,name,db_fmt):
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

    def init_db(self,db_fmt):
        # XML
        if db_fmt == "xml":
            import xml
        # YAML
        elif db_fmt == "yaml":
            import yaml
        # NETCDF
        elif db_fmt == "netcdf":
            import NetCDF4
        # CSV
        elif db_fmt == "csv":
            import csv
        # JSON
        elif db_fmt == "json":
            import json
