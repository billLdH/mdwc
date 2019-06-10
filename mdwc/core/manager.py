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
    DEPRECATED !!!!! ARGUMENTS ARE NOT READ NOW
                     EVERYTHING IS PUT INTO MD FILE
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

    main_time = time.clock()

    # SHOULD BE SET IN THE SETUP.PY (USEFUL ?)
    # subprocess.call("export MWDC_DIR=...")

    # Initialize path, directories and name
    calc= Calculator()
    name= calc.name
    wkdir= calc.wkdir

    # Start writing main output
    init_output(name)

    # Initialize Molecular Dynamics and Constraints objects
    md= MD(name,wkdir)

    # Write all tags into the main output
    # MD.write_parameters()
    # Constraints.write_parameters()

    # Initialize DFT
    DFT()
    #     dft_code= check_dft_code(mdfile,name)

    # Initialize Database
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
    #   db_fmt= check_db_packages(mdfile)
    #   db = DB(name,db_fmt)

    print("Initialization duration: ",str(datetime.timedelta(time.clock() - main_time)))

    # Run MD
    run_md(calc,md,constr,name,dft_code,datafile)

    #     # Close everything
    close_db(db)
    close_datafile(datafile)

    print("Endding date: ",strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print("Calculation duration: ",str(datetime.timedelta(time.clock() - main_time)))
    close_output_file(name)
