#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class DFTdata:
    """
    Object storing informations specific to DFT (energies,k-mesh,...)
    """
    def __init__(self):
        self.data = dict()
        self.data = {"convergence": False,
                     "e_units", "eV",
                     "etotal": 0.,
                     "entropy": 0.}

class DFT(object):
    def __init__(self,mdfile):

        dft_code = mdInput["dft_code"]
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


        self.opt_dft= mdInput["opt_dft"]
        exec_dft = mdInput["exec_dft"]
        if exec_dft is None:
            # binary in PATH
            exec_dft= dft_code
        if shutil.which(exec_dft) is None:
            _error("Executable of the DFT code does not exist.",0)

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

    def get_pressure(self):
        return

    def get_magnetic_moments(self):
        return

    def get_lattice(self):
        return

    def get_rec_lattice(self):
        return
