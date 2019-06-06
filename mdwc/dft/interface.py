#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class Calculator:
    def _init__(self,dft_code,input_para):
        self.dft_code = dft_code[0]
        self.dft_exec = dft_code[1]
        self.dft_opts = dft_code[2]
        self.calc_np = input_para["np"]
        self.calc_opts = input_para["mpi_options"]
        self.command = None

        if self.calc_np not None and
           self.calc_np > 1:
            self.command = "mpirun -np %s " % self.calc_np
            if self.calc_opts not None:
                self.command += "%s " % self.calc_opts
        else:
            self.command = ""

        self.command += "%s %s" % (self.dft_exec,self.dft_opts)

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

class DFTresults:
    def get_convergence(self):
        return

    def get_total_energy(self):
        return

    def get_atomic_positions(self):
        return

    def get_forces(self):
        return

    def get_stress_tensor(self):
        return

    def get_magnetic_moments(self):
        return

    def get_lattice(self):
        return

    def get_reciprocal_lattice(self):
        return
    

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_dft_code(data,mdfile,name):
    """
    Select DFT Code
    """
    data= open(mdfile).readlines()
    dft_code= [line for line in data if "dft_code" in line]
    if len(code) > 1:
        _exit("More than one DFT codes are given in input file.",0)
    elif len(code) < 1:
        _exit("DFT code is not given in input file.",0)
    else:
        dft_code= str(re.findall('\s*MD\s+(.*)',data)[0].split()[0])

    # ABINIT
    if dft_code in ["abinit","Abinit","ABINIT"]:
        dft_code= "abinit"
        check_abinit_files(name)
    # AIMPRO
    elif dft_code in ["aimpro","Aimpro","AIMPRO"]:
        dft_code= "aimpro"
        _exit("Not implemented yet.",0)
    # CASTEP
    elif dft_code in ["castep","Castep","CASTEP"]:
        dft_code= "castep"
        _exit("Not implemented yet.",0)
    # CP2K
    elif dft_code in ["cp2k","CP2K"]:
        dft_code= "cp2k"
        _exit("Not implemented yet.",0)
    # CRYSTAL
    elif dft_code in ["crystal","Crystal","CRYSTAL"]:
        dft_code= "crystal"
        _exit("Not implemented yet.",0)
    # ELK
    elif dft_code in ["elk","Elk","ELK"]:
        dft_code= "elk"
        _exit("Not implemented yet.",0)
    # QUANTUM ESPRESSO
    elif dft_code in ["QE","qe","quantum espresso",\
                      "Quantum Espresso","QUANTUM ESPRESSO"]:
        dft_code= "qe"
        _exit("Not implemented yet.",0)
    # SIESTA
    elif dft_code in ["siesta","Siesta","SIESTA"]:
        dft_code= "siesta"
        _exit("Not implemented yet.",0)
    # VASP
    elif dft_code in ["vasp","Vasp","VASP"]:
        dft_code= "vasp"
        _exit("Not implemented yet.",0)
    # WIEN2K
    elif dft_code in ["Wien2k","wien2k","WIEN2K"]:
        dft_code= "wien2k"
        _exit("Not implemented yet.",0)

    return dft_code

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
    """
    Create new directory and copy input files into this
    """

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
