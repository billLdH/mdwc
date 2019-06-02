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

def check_db_packages():
    """
    Check if a MD database can be created.
    """
    packages = ['xml',
                'yaml',
                'netCDF4',
                'csv',
                'json']

    db_fmt = [str(re.findall('\s*db_fmt\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('db_fmt')]

    if db_fmt in ["XML","xml"]:
        db_fmt= "xml"
        pkg= "xml"
    elif db_fmt in ["YAML","yaml"]:
        db_fmt= "yaml"
        pkg= "yaml"
    elif db_fmt in ["NETCDF","netCDF","NetCDF","netcdf"]:
        db_fmt= "netcdf"
        pkg= "NetCDF4"
    elif db_fmt in ["CSV","csv"]:
        db_fmt= "csv"
        pkg= "csv"
    elif db_fmt in ["JSON","json"]:
        db_fmt= "json"
        pkg= "json"

    try:
        import pkg
    except ImportError:
        _error(pkg+" package not installed.",0)

    return db_fmt

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
