#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import numpy as np

class Constraints:
        """
        Constraints class
        """
    def __init__(self):

        # Atoms
        self.nb_atoms = None
        self.atoms = None
        self.atom_pos = None
        self.atom_coords = None
        self.atoms_bool = None

        # Bonds
        self.nb_bonds = None
        self.bonds = None
        self.bond_dist = None
        self.bonds_bool = None

        # Angles
        self.nb_angles = None
        self.angles = None
        self.cos_angle = None
        self.angles_bool = None

        # Cell parameters (a, b, c)
        self.nb_cell_params = None
        self.cell_params = None
        self.cell_param_lgth = None
        self.cell_params_bool = None

        # Cell angles
        self.nb_cell_angles = None
        self.cell_angles = None
        self.cos_cell_angles = None
        self.cell_angles_bool = None

        # Volume
        self.vol = None
        self.vol_value = None
        self.vol_bool = None

    def get_md_constrains(self,mdfile):
        data= open(mdfile).readlines()
        for line in data:
            # Remove comment
            line = line.split('#')[0]
    
            # Bonds
        	if re.match('number_bond_constrains', line):
        	    self.nb_bonds= int(re.findall('\s*number_bond_constrains\s+(\d+)', line)[0])
        	elif re.match('bond_constrains', line) :
        	    if self.nb_bonds != 0:
        		self.bonds,unit = get_constrains_values(line,'bond_constrains', \
                                                            self.nb_bonds,int)
        	    else:
        		self.bonds= np.array([[1,2]])
        	elif re.match('bond_distance', line):
        	    if self.nb_bonds != 0:
        		self.nb_bonds,unit = get_constrains_values(line,'bond_distance', \
                                                               self.nb_bonds,float)
                    if unit == "Ang":
        		    self.bond_dist/= units["Bohr_Ang"]
        		self.bonds_bool = 1
        	    else:
        		self.bond_dist= np.array([1.00])
        		self.nb_bonds = 1
        		self.bonds_bool = 0
    
            # Atoms
            elif re.match('number_atom_fix_constrains', line):
                self.nb_atoms= int(re.findall('\s*number_atom_fix_constrains\s+(\d+)', line)[0])
            elif re.match('atom_fixed_constrains', line):
                if self.nb_atoms != 0:
            	self.atoms,unit = get_constrains_values(line,'atom_fixed_constrains',\
                                                            self.nb_atoms,int)
                else:
            	self.atoms= np.array([[1]])
            
            elif re.match('atom_fixed_position', line):
                if self.nb_atoms != 0:
            	self.atom_pos,unit = get_constrains_values(line,'atom_fixed_position', \
                                                               self.nb_atoms,float)
            	if unit == "Ang":
                        self.atom_pos/= units["Bohr_Ang"]
            	    self.atoms_bool = 1
            	else:
            	    self.atom_pos= np.array([[1.00, 1.00, 1.00]])
            	    self.nb_atoms = 1
            	    self.atoms_bool = 0
            
            elif re.match('atom_fix_coordinate', line):
                if self.nb_atoms != 0:
            	self.atom_coords,unit= get_constrains_values(line,'atom_fix_coordinate', \
                                                                 self.nb_atoms,float)
                else:
            	self.atom_coords= np.array([[1.00, 1.00, 1.00]])
    
            # Angles
    	elif re.match('number_angle_constrains', line):
    	    self.nb_angles= int(re.findall('\s*number_angle_constrains\s+(\d+)', line)[0])
    	elif re.match('angle_constrains', line):
    	    if self.nb_angles != 0:
    		self.angles,unit= get_constrains_values(line,'angle_constrains', \
                                                            self.nb_angles,int)
    	    else:
    		self.angles= np.array([[1,2,3]])
    	elif re.match('value_cosine_angle', line):
    	    if self.nb_angles != 0:
    		self.cos_angle,unit= get_constrains_values(line,'value_cosine_angle', \
                                                            self.nb_angles,float)
    		if unit == "Rad":
    		    self.cos_angle /= units["Deg_Rad"]
    		self.angles_bool = 1
    	    else:
    		self.angles= np.array([1.00])
    		self.cos_angle = 1
    		self.angles_bool = 0
    
            # Cell parameters (a, b, c)
    	elif re.match('number_cell_parameter_constrain', line):
    	    self.nb_cell_params= int(re.findall('\s*number_cell_parameter_constrain\s+(\d+)', \
                                                    line)[0])
    	elif re.match('cell_parameter_constrain', line):
    	    if self.nb_cell_params != 0:
    		self.cell_params,unit = get_constrains_values(line,'cell_parameter_constrain', \
                                                                  self.nb_cell_params,int)
    	    else:
    		self.cell_params= np.array([[1]])
    	elif re.match('cell_parameter_value', line):
    	    if self.nb_cell_params != 0:
    		self.cell_param_lgth,unit = get_constrains_values(line,'cell_parameter_value', \
                                                                self.nb_cell_params,float)
    		if unit == "Ang":
    		    self.cell_param_lgth/= units["Bohr_Ang"]
    		self.cell_params_bool = 1
    	    else:
    		self.cell_param_lgth= np.array([1.00])
    		self.nb_cell_params = 1
    		self.cell_params_bool = 0
    
            # Cell angles
    	elif re.match('number_cell_angle_constrain', line):
    	    self.nb_cell_angles= int(re.findall('\s*number_cell_angle_constrain\s+(\d+)', line)[0])
    	elif re.match('cell_angle_constrain', line):
    	    if self.nb_cell_angles != 0:
    		self.cell_angles,unit= get_constrains_values(line,'cell_angle_constrain', \
                                                                 self.nb_cell_angles,int)
    	    else:
    		self.cell_angles= np.array([[1,2]])
    	elif re.match('value_cosine_cell_angle', line):
    	    if self.nb_cell_angles != 0:
    		self.cos_cell_angles,unit= get_constrains_values(line,'value_cosine_cell_angle', \
                                                                     self.nb_cell_angles,float)
    		self.cell_angles_bool = 1
    	    else:
    		self.cos_cell_angles= np.array([1.00])
    		self.nb_cell_angles = 1
    		self.cell_angles_bool = 0
    	elif re.match('volume_constrain', line):
    	    self.vol = int(re.findall('\s*volume_constrain\s+(\d+)', line)[0])
    	elif re.match('volume_value', line):
    	    if self.vol != 0:
    		self.vol_value,unit= get_constrains_values(line,'volume_value',self.vol_value,float)
    		if unit == "Ang^3":
    		    self.vol_value/= (units["Bohr_Ang"])**3
    		self.vol_bool= 1
    	    else:
    		self.vol_value= np.array([1.00])
    		self.vol= 1
    		self.vol_bool= 0

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_constrains_values(line,tag,num,out_type):
	# Read data
	array = re.findall('\s*'+str(tag)+'\s+(.*)', line)[0].split(',')
	array.remove('')
	# Check if unit is given
	unit = None
	if not array[-1].replace('.','',1).isdigit():
		unit= array[-1].split()[-1]
		array[-1].replace(unit,'')
	if len(array[0]) == 1:
		array= np.array(map(out_type,array[:num]))
	else:
		array= np.array([map(out_type,item.split()) for item in array[:num]])
	return array,unit

