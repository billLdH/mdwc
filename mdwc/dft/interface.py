#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

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
    elif dft_code in ["quantum espresso","Quantum Espresso",\
                      "QUANTUM ESPRESSO"]:
        dft_code= "quantum espresso"
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

