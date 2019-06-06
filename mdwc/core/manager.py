#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import shutil
import numpy as np
import argparse
import time
from time import time, strftime, localtim
import datetime
from mdwc.dft import *
from mdwc.io.outputs import create_output,init_datafile,
                            close_datafile,Data
from mdwc.utils.info import Info
from mdwc.io.db import *
from mdwc.dft.interface import Calculator
from mdwc.utils.checks import *

def get_arguments:
    """
    Read arguments
    """
    parser = argparse.ArgumentParser(description='Paramenters for MD')
    parser.add_argument("-n", "--name",
    		        nargs=1,
    		        help="Name of the input file.md.",
    		        dest="name",
    		        type=str,
    		        required=False)
    parser.add_argument("-npt",
                        nargs=0,
                        help="NPT Molecular Dynamics (default)",
                        dest="npt",
                        required=False)
    parser.add_argument("-nvt",
                        nargs=0,
                        help="NVT Molecular Dynamics",
                        dest="nvt",
                        required=False)
    parser.add_argument("-np", "--ntasks",
                        nargs=1,
                        help="Number of tasks for mpirun",
                        dest="ntasks",
                        type=int,
                        required=False)
    parser.add_argument("-mopt", "--mpi_options",
                        nargs=1,
                        help="Additional mpirun options",
                        dest="mpi_options",
                        type=str,
                        required=False)
    
    input_para= vars(parser.parse_args())
   
    return input_para

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def main():
    """
    Main
    """
    # Header
    info = Info("../PACKAGE_INFO.txt")
    start_message(info)
    get_system_info()
    get_python_info()
    
    # Time
    main_time = time.clock() 

    # Checks arguments and if input files are here
    check_python_env()
    quick_check()
    input_para = get_arguments()
    name= check_filename(input_para)
    mdfile= name+".md"
    # readMDIn()
    mdtype= check_md_type(input_para,mdfile)
    dft_code= check_dft_code(mdfile,name)

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
    db = DB(name,db_fmt)

    # Initialize calculator
    calc= Calculator(dft_code,input_para)

    # Initialize outputs
    datafile = Data(name)
    init_datafile(datafile,md)
    stdout= create_output(name,db_fmt)
    info= Info("PACKAGE_INFO.txt")
    start_message(info)

    # Set Molecular Dynamics
    md = mdwc_manager.MD(mdfile,mdtype,dft_code[0])
    md.get_md_parameters()
    md.total_steps= md.md_steps*md.dft_steps
    md.temp_data_reader(md.total_steps)
    # write_output()
    # write_db() <---- Needs an interface

    # Set Constraints
    constr = mdwc_manager.Constraints(md.mdfile)
    constr.get_md_constrains()
    # write_output()
    # write_db() <---- Needs an interface
    print("Initialization duration: ",str(datetime.timedelta(time.clock() - main_time)))

    # Run MD
    run_md(calc,md,constr,name,dft_code,datafile)

    # Close everything
    close_output_file(name)
    close_db(db)
    close_datafile(datafile)
   
    # Time
    print("Endding date: ",strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print("Calculation duration: ",str(datetime.timedelta(time.clock() - main_time)))
