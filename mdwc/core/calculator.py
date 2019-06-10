#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class Calculator(MD,Database,DFT):
    """
    Calculator object (manager of the calculation)
    """
    def initialize(self):
        self.command = None

        # self.command += "%s %s" % (self.dft_exec,self.dft_opts)

        """
        Initialize the calculation
        1) Get main name
        2) Create a working directory
         WKDIR
            |
            |- INPUT FILES
            |
            |- SUBWKDIR1
            |
            |- SUBWKDIR2
            .
            .
        """
        # Starting time
        self.start_time= time.clock()

        # Quick checks
        check_python_env()
        # quick_check() DEPRECATED !!! EVERYTHING IS INTO THE MD FILE

        # Read arguments and md file
        self.name= check_filename()
        wkdir= "mdwc_"+name
        p= subprocess.call("mkdir %s" % wkdir, shell=True)
        p.wait()
        self.path= os.getcwd()
        self.wkdir= self.path+"/"+wkdir
        p= subprocess.call("cp %s %s" % (self.name,self.wkdir))
        p.wait()

        # Initialize output
        self.stdout= init_output(name)

        # Initialize Molecular Dynamics and Constraints objects
        MD.__init__(name,wkdir)

        # Initialize Database
        DB.__init__(MD.mdInput,name)

        # Initialize DFT
        DFT.__init__(MD.mdInput,name)

    def init_db(self):
        """
        Initialize DB object
        """
        # Check if storage in db is possible (YAML, XML, JSON, CSV, NetCDF)
        # In this db file, we could store for each step (few ideas):
        #   - MD info (Qmass, Bmass, dt, species, psp, natom,...) <= only once
        #   - Energy
        #       # DFT
        #       # Constraints' cost ?
        #   - Pressure
        #   - Temperature
        #   - Atomic positions (reduced and cartesian)
        #   - Cell (parameters and angles)
        #   - Volume
        #   - Stress tensor
        #   - Forces (atoms, cell,...)
        db_fmt= check_db_packages(mdfile)

    def run(self):
        Popen()
        poll
        wait

    def get_dft_code(self):
        return self.dft_code

    def get_dft_exec(self):
        return self.dft_exec

    def get_dft_opts(self):
        return self.dft_opts

    def get_calc_np(self):
        return self.calc_np

    def get_calc_opts(self):
        return self.calc_opts

    def get_command(self):
        return self.command

    def set_dft_code(self,dft_code):
        self.dft_code= dft_code

    def set_dft_exec(self,dft_exec):
        self.dft_exec= dft_exec

    def set_dft_opts(self,dft_opts):
        self.dft_opts= dft_opts

    def set_calc_np(self,calc_np):
        self.calc_np= calc_np

    def set_calc_opts(self,calc_opts):
        self.calc_opts= calc_opts

    def set_command(self,command):
        self.command= command

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def initialize_md(name):
    # Read md files
    mdfile= name+".md"
    # readMDIn() should replace following lines and put everything into a dict
    self.mdtype= check_md_type(self.input_para,self.mdfile)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def initialize_dft(self):
    """
    Initialize DFT object
    """
    self.dft_code= check_dft_code(self.mdfile,self.name)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir(name, xred, h, step, pwd= None):
    """
    Create new directory and copy input files into this
    """
    directory = name+str(step)
    subprocess.call('mkdir %s' % directory, shell=True)
    [subprocess.call('cp %s %s/' % (f_in,directory)) for f_in in inputs]

# * * * * * * * * * * * * * * * * * * * * * * * * * *
