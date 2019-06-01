#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import time
import subprocess
import argparse
import mdwc.MD_suite.MD_suite as md_ft
import mdwc.software_tools.abinit_controller as ac


def _error(message,code):
	""" 
        Print error message and exit
        """
	print(message)
	exit(code)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check():
	""" 
 	Check options 
	"""

	options = ["-h", "-help", "-n", "--name", "-npt", "-nvt", 
                   "-np", "--ntasks", "-mopt", "--mpi_options"]

	if len(sys.argv) < 2:
		_error("Sub-command are needed. Type 'mdwc_ -h' for printing helps.",0)

	if len(set(sys).intersection(options)) < 1:
		_error("Wrong sub-commands. Type 'mdwc_ -h' for printing helps.",0)
	
	input_para, name = read_arguments()

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def read_arguments:
	parser = argparse.ArgumentParser(description='Paramenters for MD')
	parser.add_argument("-n", "--name",
			    nargs=1,
			    help="Name of the .in, .files, .md files",
			    dest="name",
			    type=str,
			    required=True)
        parser.add_argument("-c", "--dft_code",
                            nargs=1,
                            help="DFT code.",
                            dest="code",
                            type=str,
                            required=True)
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

	if input_para['name'] is None:
		name=[file for file in os.listdir(".") if file.endswith('.in')]
		if len(name) > 2:
			_error("Please set name of files adding '-n [NAME]'.")
		else:
			name=str(name[0])
	else:
		name= input_para['name']
	return input_para, name

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def main():

        # MD file
        mdfile = name+'.md'
        
        # Check arguments and read name.md file
        check()
        input_para, name = read_arguments()
        read_input()

        # Get Molecular Dynamics parameters
        md = mdwc_manager.MD(mdfile)
        md.get_md_parameters()
        md.total_steps= md.md_steps*md.dft_steps
        md.temp_data_reader(md.total_steps)

        # Get Constraints parameters
        constr = mdwc_manager.Constraints(md.mdfile)
        constr.get_md_constrains()

        # Create output file
        pressure_volu_file= open('pressure_volume.mdout', 'w')
        pressure_volu_file.write( \
          'md_step     dft_step     total_step    time(fs)     pressure(hartree/Bohr^3)     volume(Bohr^3)\n')

numb_bond_cons, bool_bond_cons, numb_angl_cons, bool_angl_cons, \
numb_cell_para_cons, bool_cell_para_cons, numb_cell_angl_cons, bool_cell_angl_cons,\
volu_cons , bool_volu, numb_atom_fix_cons, bool_atom_fix_cons, bond_const, angl_const, cell_para_const,\
cell_angl_const, atom_fix_const, bond_valu, angl_valu, cell_para_valu,\
cell_angl_valu, volu_valu, atom_fix_valu, atom_fix_cord= ac.get_md_constrains(name+'.md')


