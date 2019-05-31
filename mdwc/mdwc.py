#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
NAME
	mdwc_ - Molecular Dynamics With Constraints

DESCRIPTION
  	   The molecular dynamics with constraints (mdwc) package is a 
	command line open source python program. It does constraint 
	molecular dynamics following the SHAKE algorithm with:
   	    - NPT: keeping pressure constant with the Parrinello-Rahman 
          	   lagrangian, and keeping the temperature constant 
		   with the Nose thermostat) 
   	    - NVT: keeping the temperature constant with the Nose thermostat. 

	Constraints:
   	    - bond distances
   	    - angles
   	    - atomic positions
   	    - lattice parameters (a, b, c)
   	    - angles between lattice vectors
   	    - volume of the unit cell.

	Supported DFT codes:
	    - Abinit

SYNTAX
	mdwc_ <sub-command> [OPTIONS]

SUB-COMMANDS

   # ----- Help ----------------------------------

        -h, -help
	    print this help

   # ----- Files Manager -------------------------

	-n, --name [NAME]

   # ----- Molecular Dynamics Manager ------------

        -npt
            Run NPT Molecular Dynamics (default)

	-nvt
	    Run NVT Molecular Dynamics

   # ----- MPI -----------------------------------

	-np, --ntasks [NUMBER_OF_TASKS]
	    Number of tasks for mpi parallelization

	-mopt, --mpi_options "[OPTIONS]"
	    Add more options for mpirun

REQUIREMENTS
	- Python 3
	- Numpy >= 1.1 1
	- DFT Code 

LINKS
        GitHub - https://github.com/romerogroup/mdwc.git
        Documentation - https://molecular-dynamics-with-constraints.github.io/

"""

__name__="mdwc"
__version__ =1.0.0
__author__ = "Aldo H. Romero, Arturo Hernandez, Uthpala Herath, Pedram Tavazohi"
#__licence__ = ""  <----- TO BE SET
__maintainer__ ="Aldo H. Romero"
__maintainer_email__ ="Aldo.Romero@mail.wvu.edu"
__description__="Molecular Dynamics With Constraints"
__date__ = "June 2019"
__url__="https://molecular-dynamics-with-constraints.github.io/"
__download_url__="https://github.com/romerogroup/mdwc.git"


#          + + + + + + + + +
# + + + + +     MODULES     + + + + +
#          + + + + + + + + +


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

#          + + + + + + + +
# + + + + +    CLASSES    + + + + +
#          + + + + + + + + 


#          + + + + + + + +
# + + + + +   FUNCTIONS   + + + + +
#          + + + + + + + + 

def _error(message,code):
	""" 
        Print error message and exit
        """
	print(message)
	exit(code)

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

def read_arguments:
	parser = argparse.ArgumentParser(description='Paramenters for MD')
	parser.add_argument("-n", "--name",
			    nargs=1,
			    help="Name of the .in, .files, .md files",
			    dest="name",
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

#-------------------
#   GET MD PARAM.
#-------------------
Qmass, bmass, P_ext, dt, correc_steps, md_steps, abinit_steps= ac.get_md_parameters(name+'.md')
numb_bond_cons, bool_bond_cons, numb_angl_cons, bool_angl_cons, \
numb_cell_para_cons, bool_cell_para_cons, numb_cell_angl_cons, bool_cell_angl_cons,\
volu_cons , bool_volu, numb_atom_fix_cons, bool_atom_fix_cons, bond_const, angl_const, cell_para_const,\
cell_angl_const, atom_fix_const, bond_valu, angl_valu, cell_para_valu,\
cell_angl_valu, volu_valu, atom_fix_valu, atom_fix_cord= ac.get_md_constrains(name+'.md')
md_total_steps= md_steps*abinit_steps
temp_arra= ac.temp_data_reader(name+'.md', md_total_steps)
pressure_volu_file= open('pressure_volume.mdout', 'w')
pressure_volu_file.write('md_step     abinit_step     total_step    time(fs)     pressure(hartree/Bohr^3)     volume(Bohr^3)\n')

#------------------
#   START LOOPS
#------------------
for i_abinit_step in range(abinit_steps):
	temp= temp_arra[i_abinit_step*md_steps]
	print 'abinit step  ', i_abinit_step
	if i_abinit_step == 0:
		s_t=1.0 #thermostat degree of freedom
		s_t_dot= 0.0#time derivative of thermostat degree of freedom
		#First abinit run. Take the prototype xxxx.in and xxxx.files
		#and put them in what is going to be the working directory
		work_dir= name+str(i_abinit_step)
		subprocess.call(['mkdir', work_dir])
		ac.from_prototype_in_to_in_step0(name+'.in', work_dir+'/'+name+str(i_abinit_step)+'.in')
		ac.from_prototype_file_to_file(name+'.files', work_dir+'/'+name+str(i_abinit_step)+'.files', i_abinit_step)
	else:
		work_dir= ac.create_directories(name, x_t, h_t, i_abinit_step, pwd='.')
	rf= open(work_dir+'/'+name+str(i_abinit_step)+'.files')
	log= open(work_dir+'/'+name+str(i_abinit_step)+'.log','w')
	#        job= subprocess.Popen('mpirun -np 4 abinit', bufsize=1048576, shell=True, \
	#                              stdout=log, stdin=rf, cwd=work_dir)
	if input_para['mpirum'] == True:
		comand_string='mpirun -np %d abinit' %input_para['np'] 
		job= subprocess.Popen(comand_string, bufsize=1048576, shell=True,\
		stdout=log, stdin=rf, cwd=work_dir)
	else:
		job= subprocess.Popen('abinit', bufsize=1048576, shell=True,\
		stdout=log, stdin=rf, cwd=work_dir)
	n=0
	while job.poll() == None:
		#print job.poll()
		time.sleep(30)
		if os.path.exists(work_dir+'/'+name+str(i_abinit_step)+'.out'):
			output= open(work_dir+'/'+name+str(i_abinit_step)+'.out','r')
			data= output.read()
			match= re.search('Calculation\s+completed', data)
			if match and n == 0:
				job.kill()
				n=1
	#end if match and n == 0:
	#print job.poll()
	nat, mass, h_t, strten_in= \
	ac.get_nat_mass_latvec_in_strten_in(work_dir+'/'+name+str(i_abinit_step)+'.out')
	x_t, f_t= ac.get_xred_fcart(work_dir+'/'+name+str(i_abinit_step)+'.out', nat)
	#h_t_inv= np.linalg.inv(h_t)
	#F_redu_t= np.dot(h_t_inv, f_t)
	#out= md.md_npt_step(dt, md_steps, mass, Qmass, bmass, temp, correc_steps, x_t, x_t_dot, v_t, F_redu_t,\
	#            h_t, h_t_dot, strten_in, P_ext, s_t, s_t_dot)

        #---------------
        #   INIT VEL.
        #---------------
	if i_abinit_step == 0:
		# Initialization of velocities
		v_t= md_ft.npt_md_suite.init_vel_atoms(mass, temp, len(mass))
		h_t_dot= md_ft.npt_md_suite.init_vel_lattice(bmass, temp, h_t)
		x_t_dot= md_ft.npt_md_suite.get_x_dot(h_t, v_t, nat)

	#--------------
	#   RUN  NPT
	#--------------
	if not input_para['NVT'] or input_para['NPT']:
		s_t, s_t_dot, pressure_t, volu_t,\
		bond_constrain_t, cos_constrain_t, h_t,\
		h_t_dot, x_t, x_dot_t, v_t= \
                         md_ft.npt_md_suite.md_npt_constrains(h_t,x_t, \
				x_t_dot, f_t, strten_in,v_t,h_t_dot,\
				bond_valu, angl_valu, cell_para_valu,\
				cell_angl_valu, volu_valu, atom_fix_valu,atom_fix_cord,\
				P_ext,mass,\
				Qmass, bmass, dt, temp, s_t, s_t_dot, \
				bond_const,angl_const, cell_para_const,\
				cell_angl_const, atom_fix_const,correc_steps, md_steps,\
				bool_bond_cons,bool_angl_cons,\
				bool_cell_para_cons,bool_cell_angl_cons,\
				bool_volu,bool_atom_fix_cons,volu_cons, nat, \
				numb_cell_angl_cons,numb_cell_para_cons,\
				numb_angl_cons, numb_bond_cons,numb_atom_fix_cons)    
		write_md_output(work_dir+'/'+name+str(i_abinit_step)+'.mdout',\
			bond_const, angl_const, pressure_t, volu_t, bond_constrain_t, cos_constrain_t)
		for i,_ in enumerate(pressure_t):
			md_time= (i_abinit_step*md_steps+i)*dt
			#pressure_volu_file.write('md_step     abinit_step     total_step    time(fs)     pressure(hartree/Bohr^3)     volume(Bohr^3)\n')
			pressure_volu_file.write('%d          %d               %d             %.3f         %.3E                         %.3f\n'\
			%(i+1,i_abinit_step+1,(i_abinit_step*md_steps+i+1),md_time,pressure_t[i],volu_t[i]))
	else:
        #--------------
        #   RUN  NVT
        #--------------

		s_t, s_t_dot, x_t, v_t= md_ft.npt_md_suite.md_nvt_constrains(h_t,x_t, \
				f_t,v_t,\
				bond_valu, angl_valu,\
				atom_fix_valu,atom_fix_cord,mass,\
				Qmass, dt, temp, s_t, s_t_dot,\
				bond_const,angl_const,\
				atom_fix_const,correc_steps, md_steps,\
				bool_bond_cons,bool_angl_cons,\
				bool_atom_fix_cons, nat,\
				numb_angl_cons, numb_bond_cons,numb_atom_fix_cons)
pressure_volu_file.close()


#          + + + + + + +
# + + + + +     MAIN    + + + + +
#          + + + + + + + 

if __name__ == "__main__":
	check()
	read_input()
	run_md()
