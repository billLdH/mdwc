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
from mdwc.info import Info
from mdwc.io.db import *
from mdwc.dft.interface import Calculator

def _error(message,code):
    """ 
    Print error message and exit
    """
    print(message)
    exit(code)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check():
    """ 
    Check options and if file.md exists
    """
    
    options = ["-h", "-help", "-n", "--name", "-npt", "-nvt", 
               "-np", "--ntasks", "-mopt", "--mpi_options"]
    
    if len(sys.argv) < 2:
    	_error("Sub-command are needed. Type 'mdwc_ -h' for printing helps.",0)
    
    if len(set(sys).intersection(options)) < 1:
    	_error("Wrong sub-commands. Type 'mdwc_ -h' for printing helps.",0)

    if len([file for file in os.listdir(".") if file.endswith('.md')]) < 1:
        _error("File.md is missing.",0)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def read_arguments:
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

def check_files(input_para):
    """
    Check if all needed files exist
    """

    # MD file
    mdfiles = [file for file in os.listdir(".") if file.endswith('.md')]
    if input_para['name'] is None:
        if len(mdfiles) > 2:
            _error("Please set name of files adding '-n [NAME]'.",0)
        elif len(mdfiles) < 1:
            _error("File.md does not exist in the directory.",0)
        else:
            name= str(mdfiles[0])
    else:
        name= str(input_para['name'])
        if name+".md" not in os.listdir("."):
            _error(name+".md does not exist in the directory.",0)
    mdfile = name+".md"

    # MD type
    if input_para["npt"] is None and input_para["nvt"] is None:
        data= open(mdfile).readlines()
        for line in data:
        mdtype= [str(re.findall('\s*MD\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('MD')]
        if len(mdtype) != 0:
            _error("MD type is not set correctly.",0)
        else:
            if mdtype[0] in ["NPT","npt"]:
                mdtype= "npt"
            elif mdtype[0] in ["NVT","nvt"]:
                mdtype= "nvt"
            else:
                _error("MD type is not set correctly.",0)
    elif input_para["npt"] is not None and input_para["nvt"] is not None
        _error("MD type is not set correctly.",0)
    elif input_para["npt"] is not None:
        mdtype= "npt"
    elif input_para["nvt"] is not None:
        mdtype= "nvt"

    # DFT Code
    dft_code.append(interface.get_dft_code(data,mdfile,name))

    # Absolute path to a pecific executable of the DFT code
    exec_dft = [str(re.findall('\s*exec_dft_code\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('exec_dft_code')]
    if len(exec_dft) > 1:
        _error("Executable of the DFT code not set properly.",0)
    elif len(exec_dft) < 1:
        # binary in PATH
        exec_dft= dft_code  
    else:
        # Specific executable
        exec_dft= str(exec_dft[0])

    if shutil.which(exec_dft) is None:
        _error("Executable of the DFT code does not exist.",0)
    dft_code.append(exec_dft)

    # DFT Code options
    opt_dft = [str(re.findall('\s*opt_dft_code\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('opt_dft_code')]

    dft_code.append(opt_dft)
    return name, mdfile, mdtype, dft_code

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def main():
    """
    Main
    """
    # Time
    main_time = time.clock() 

    # Checks arguments and if input files are here
    check()
    input_para = read_arguments()
    name, mdfile, mdtype, dft_code= check_files(input_para)
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
