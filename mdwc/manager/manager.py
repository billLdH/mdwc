#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *
from mdwc.manager.outputs import *

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
                        dest="NPT",
                        required=False)
    parser.add_argument("-nvt",
                        nargs=0,
                        help="NVT Molecular Dynamics",
                        dest="NVT",
                        required=False)
    parser.add_argument("-np", "--ntasks",
                        nargs=1,
                        help="Number of tasks for mpirun",
                        dest="ntasks",
                        type=str,
                        required=False)
    parser.add_argument("-mopt", "--mpi_options",
                        nargs=1,
                        help="Name of the .in, .files, .md files",
                        dest="Additional mpirun options",
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

    # DFT Code
    dft_code= interface.dft_code(data,mdfile,name)

    # Absolute path to a pecific executable of the DFT code
    exec_dft= [line for line in data if "exec_dft_code" in line]
    if len(exec_dft) > 1:
        _error("Executable of the DFT code not set properly.",0)
    elif len(exec_dft) < 1:
        # binary in PATH
        exec_dft= dft_code  
    else:
        # Specific executable
        exec_dft= str(exec_dft[0])

    return name, mdfile, dft_code, exec_dft

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def main():
    """
    Main
    """
    
    # Check arguments and if input files are here
    check()
    input_para = read_arguments()
    name, mdfile, dft_code, exec_dft= check_files(input_para)

    # Start printing and writting informations
    create_output_file(name)
    start_message()

    # Set Molecular Dynamics
    md = mdwc_manager.MD(mdfile)
    md.get_md_parameters()
    md.total_steps= md.md_steps*md.dft_steps
    md.temp_data_reader(md.total_steps)

    # Set Constraints
    constr = mdwc_manager.Constraints(md.mdfile)
    constr.get_md_constrains()

    # Run MD
    run_md(md,constr,name,dft_code,exec_dft)

    # Create output file
    pressure_volu_file= open('pressure_volume.mdout', 'w')
    pressure_volu_file.write( \
      'md_step     dft_step     total_step    time(fs)     pressure(hartree/Bohr^3)     volume(Bohr^3)\n')
   
    # Close the main output file
    close_output_file(name)
