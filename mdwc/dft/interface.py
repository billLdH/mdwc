#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class DFT:
    def __init__(self,mdfile):
        sefl.mdfile = mdfile

        data= open(mdfile).readlines()
        dft_code= [line for line in data if "dft_code" in line]
        if len(code) > 1:
            _error("More than one DFT codes are given in input file.",0)
        elif len(code) < 1:
            _error("DFT code is not given in input file.",0)
        else:
            dft_code= str(re.findall('\s*dft_code\s+(.*)',data)[0].split()[0])

        # ABINIT
        if dft_code in ["abinit","Abinit","ABINIT"]:
            self.dft_code= "abinit"
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

    def get_convergence(self):
        return

    def get_total_energy(self):
        return

    def get_cart_positions(self):
        return

    def get_red_positions(self):
        return

    def get_cart_forces(self):
        return

    def get_stress_tensor(self):
        return

    def get_magnetic_moments(self):
        return

    def get_lattice(self):
        return

    def get_rec_lattice(self):
        return
    
    def initialize_dft():
    """
    Create new directory and copy input files into this
    """


# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
    """
    Create new directory and copy input files into this
    """

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
