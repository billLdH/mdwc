#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import sys
from time import time, strftime, localtime
from netCDF4 import Dataset
from mdwc.info import Info
from mdwc.io.db import *
from mdwc.utils.timer import today_txt
import numpy as np

def init_datafile(datafile,md):
    """
    Initialize data file (default output)
    """

    datafile.data = open(datafile.datafile")
    data.data.write("#%8s %8s %7s %7s%5s %8s %6s %4s %13s %9s"
        % ("time(fs)", "tot_step", "md_step", md.dft_code, "_step",
           "E(har)", "T(K)", "P(har/Bohr^3)", "V(Bohr^3)")

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_output(name):
    """
    Initialize main output
    """
    # Main
    out = sys.stdout
    stdout = open(name+'.out_md', 'w')
    sys.stdout = stdout

    # Header
    # TO BE SET: $MDWC variables
    info = Info("$MDWC/PACKAGE_INFO.txt")
    start_message(info)
    get_system_info()
    get_python_info()

    return stdout

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def close_output_file(stdout):
    sys.stdout = stdout
    stdout.close()


# * * * * * * * * * * * * * * * * * * * * * * * * * *

def start_message(info):
    """
    Start message
    """
    print("""
 Starting date: %s     

      __   __    ____     _   _   _    _____
     |  \ /  |  |    \   | | | | | |  |  ___| 
     |   |   |  | |\  \  |  \| |/  |  | |
     | |\_/| |  | |/  /   \       /   | |___
     | |   |_|  |____/      \_/\_/    |_____|
     |
     |  Molecular Dynamics With Constraints
      \_____________________________________/

 %s 
 Version %s (%s)
 License %s

 Authors: %s
 Contact: %s (%s)
          %s
 Download url: %s
 Official Web site: %s

    """   % (today_txt(),
             info.__name__, \
             info.__version__, \
             info.__date__, \
             info.__license__, \
             info.__author__, \
             info.__maintainer__, \
             info.__university__, \
             info.__maintainer_email__, \
             info.__download_url__, \
             info.__url__) 
           )

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def end_message():
    """
    End message
    """

# * * * * * * * * * * * * * * * * * * * * * * * * * *

# NEED TO BE MODIFIED
def write_md_output(path, bond_const, angl_const, pressure_t, volu_t, bond_constrain_t, cos_constrain_t):
    mdout_file= open(path, 'w')
    mdout_file.write('md_step     volume(Bohr^3)\n')
    for i,valu in enumerate(volu_t):
            mdout_file.write('%d          %.3f\n'%(i, valu))
    mdout_file.write('\n')
    mdout_file.write('md_step     pressure(hartree/Bohr^3)\n')
    for i,valu in enumerate(pressure_t):
            mdout_file.write('%d          %.3E\n'%(i, valu))
    mdout_file.write('\n')
    mdout_file.write('bond constraints\n')
    for md_i in range(bond_constrain_t.shape[0]):
            mdout_file.write('md_step   %d\n'% md_i)
            mdout_file.write('atoms in bond     bond value\n')
            for j in range(bond_constrain_t.shape[1]):
                    mdout_file.write('%d  %d            %.3f\n'%(bond_const[j,0],\
                    bond_const[j,1], bond_constrain_t[md_i, j]**0.5))
    mdout_file.write('\n')
    mdout_file.write('angle constraints\n')
    for md_i in range(cos_constrain_t.shape[0]):
            mdout_file.write('md_step   %d\n'% md_i)
            mdout_file.write('atoms in angle constraint     cos of angle value\n')
            for j in range(cos_constrain_t.shape[1]):
                    mdout_file.write('%d  %d  %d                      %.3f\n'%(angl_const[j,0],\
                    angl_const[j,1], angl_const[j,2], cos_constrain_t[md_i, j]))
    mdout_file.close()
    return
