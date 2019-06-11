#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class Calculator(MD,Database,DFT,Structure):
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

        # Molecular Dynamics and Constraints object
        MD.__init__(self,self.mdInput)
        Constraints.__init__(self,self.name,self.wkdir)

        # Database object
        db_fmt= check_db_packages(mdfile)
        DB.__init__(self,self.name,db_fmt)

        # DFT and Structure objects
        init_dft_code(self,mdInput)
        DFT.__init__(self,self.mdInput,self.name)
        Structure.__init__(self,self.dft)
        #return md, constr, db, dft, struct

    def init_dft_code(self,mdInput):
        dft_code= mdInput["dft_code"]
        if len(code) > 1:
            _error("More than one DFT codes are given in input file.",0)
        elif len(code) < 1:
            _error("DFT code is not given in input file.",0)
        else:
            dft_code= str(dft_code)

        # ABINIT
        if dft_code in ["abinit","Abinit","ABINIT"]:
            self.dft_code= "abinit"
            self.dft= DFT(Abinit)
        # AIMPRO
        elif dft_code in ["aimpro","Aimpro","AIMPRO"]:
            self.dft_code= "aimpro"
            _error("Not implemented yet.",0)
        # CASTEP
        elif dft_code in ["castep","Castep","CASTEP"]:
            self.dft_code= "castep"
            _error("Not implemented yet.",0)
        # CP2K
        elif dft_code in ["cp2k","CP2K"]:
            self.dft_code= "cp2k"
            _error("Not implemented yet.",0)
        # CRYSTAL
        elif dft_code in ["crystal","Crystal","CRYSTAL"]:
            self.dft_code= "crystal"
            _error("Not implemented yet.",0)
        # ELK
        elif dft_code in ["elk","Elk","ELK"]:
            self.dft_code= "elk"
            _error("Not implemented yet.",0)
        # QUANTUM ESPRESSO
        elif dft_code in ["QE","qe","quantum espresso",\
                          "Quantum Espresso","QUANTUM ESPRESSO"]:
            self.dft_code= "qe"
            _error("Not implemented yet.",0)
        # SIESTA
        elif dft_code in ["siesta","Siesta","SIESTA"]:
            self.dft_code= "siesta"
            _error("Not implemented yet.",0)
        # VASP
        elif dft_code in ["vasp","Vasp","VASP"]:
            self.dft_code= "vasp"
            _error("Not implemented yet.",0)
        # WIEN2K
        elif dft_code in ["Wien2k","wien2k","WIEN2K"]:
            self.dft_code= "wien2k"
            _error("Not implemented yet.",0)

        self.opt_dft= mdInput["opt_dft"]
        exec_dft = mdInput["exec_dft"]
        if exec_dft is None:
            # binary in PATH
            self.exec_dft= dft_code
        else:
            self.exec_dft= exec_dft
        if shutil.which(exec_dft) is None:
            _error("Executable of the DFT code does not exist.",0)


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
