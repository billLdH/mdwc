#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import numpy as np

class DB:
        """
        Database class
        """
    def __init__(self,name,db_fmt):

        self.db_fmt = db_fmt
        self.db_file = None

    def get_db_filename(db_fmt,name):
        if db_fmt == "xml":
            self.db_file= name+".xml"
        elif db_fmt == "yaml":
            self.db_file= name+".yaml"
        elif db_fmt == "netcdf":
            self.db_file= name+".nc"
        elif db_fmt == "csv":
            self.db_file= name+".csv"
        elif db_fmt == "json":
            self.db_file= name+".json"

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def open_db(db):
    """
    Interface to open db file
    """
    if db.db_fmt == "xml":
        # Function in xml.py
    elif db.db_fmt == "yaml":
        # Function in yaml.py
    elif db.db_fmt == "netcdf":
        # Function in netcdf.py
    elif db.db_fmt == "csv":
        # Function in csv.py
    elif db.db_fmt == "json":
        # Function in json.py 

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_db(db,constr,md):
    """
    Interface to write dimensions, variables,... in db file
    """
    if db.db_fmt == "xml":
        # Function in xml.py
    elif db.db_fmt == "yaml":
        # Function in yaml.py
    elif db.db_fmt == "netcdf":
        # Function in netcdf.py
    elif db.db_fmt == "csv":
        # Function in csv.py
    elif db.db_fmt == "json":
        # Function in json.py

# * * * * * * * * * * * * * * * * * * * * * * * * * *
def store_db(db,md):
    """
    Interface to write md step data in db file
    """
    if db.db_fmt == "xml":
        # Function in xml.py
    elif db.db_fmt == "yaml":
        # Function in yaml.py
    elif db.db_fmt == "netcdf":
        # Function in netcdf.py
    elif db.db_fmt == "csv":
        # Function in csv.py
    elif db.db_fmt == "json":
        # Function in json.py

# * * * * * * * * * * * * * * * * * * * * * * * * * *
def close_db(db):
    """
    Interface to close db file
    """
    if db.db_fmt == "xml":
        # Function in xml.py
    elif db.db_fmt == "yaml":
        # Function in yaml.py
    elif db.db_fmt == "netcdf":
        # Function in netcdf.py
    elif db.db_fmt == "csv":
        # Function in csv.py
    elif db.db_fmt == "json":
        # Function in json.py
