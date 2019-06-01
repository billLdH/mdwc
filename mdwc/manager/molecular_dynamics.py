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


class MD:
    """
    Molecular Dynamics class
    """
    def __init__(self,path_to_file):

        # Input MD parameters
        self.mdfile = path_to_file
        self.type = None
        self.code = None
        self.qmass = None
        self.bmass = None
        self.dt = None
        self.pressure = None
        self.correct_spteps = None
        self.md_steps = None
        self.dft_steps = None
        self.total_steps = None
        self.temp = None

        def get_md_parameters(self):
            data= open(self.mdfile).read()
            # Barostat and Thermostat masses
            self.qmass= float(re.findall('\s*Qmass\s+(.*)',data)[0].split()[0])
            self.bmass= float(re.findall('\s*bmass\s+(.*)',data)[0].split()[0])
            # Pressure
            self.pressure= float(re.findall('\s*Pressure\s+(.*)',data)[0].split()[0])
            if len(re.findall('\s*Pressure\s+(.*)',data)[0].split()) > 1:
                if str(re.findall('\s*Pressure\s+(.*)',data)[0].split()[1]) == "GPa":
                        self.pressure /= units["HaBohr3_GPa"]
                elif str(re.findall('\s*Pressure\s+(.*)',data)[0].split()[1]) == "kbar":
                        self.pressure /= units["HaBohr3_kbar"]
            # Time step
            self.dt= float(re.findall('\s*dt\s+(.*)',data)[0].split()[0])
            if len(re.findall('\s*dt\s+(.*)',data)[0].split()) > 2:
                if str(re.findall('\s*dt\s+(.*)',data)[0].split()[1]) == "au":
                        self.dt *= units["au_fs"]
            # MD steps
            self.correct_spteps= int(re.findall('\s*correct_spteps\s+(.*)',data)[0].split()[0])
            self.md_steps= int(re.findall('\s*md_steps\s+(.*)',data)[0].split()[0])
            self.dft_steps= int(re.findall('\s*dft_steps\s+(.*)',data)[0].split()[0])


        def temp_data_reader():
            data_file= open(self.mdfile, 'r')
            data_file= data_file.readlines()
        
            patt_cons = re.compile('^temp_cons')
            n_cons=0
            patt_line = re.compile('^temp_line')
            n_line=0
            patt_plat = re.compile('^temp_plat')
            n_plat=0
            for string in data_file:
                if patt_cons.search(string):
                    n_cons=1
                if patt_line.search(string):
                    n_line=1
                if patt_plat.search(string):
                    n_plat=1
            data_file= str(data_file)
            indicator= n_cons + n_line + n_plat
            if indicator == 0:
                print 'select a type of temperature control'
                temp_arra=[]
                return temp_arra
            elif indicator == 1:
                if n_cons == 1:
                    temp= re.findall('\s*temp_cons\s+(.*)',data_file)[0].split(" ")
                    if not temp[-1].replace('.','',1).isdigit(): # Unit is given
                        unit = temp[-1]
                        temp= float(temp[0])
                        if unit == "C":
                                temp= temp+units["C_K"]
                    else:
                        temp= float(temp[0])
                    arra= np.ones(md_total, dtype=float)
                    temp_arra= temp*arra
                    return temp_arra
                elif n_line == 1:
                    temp= re.findall('\s*temp_line\s+(.*)',data_file)[0].split(",")
                    if not temp[-1].replace('.','',1).isdigit(): # Unit is given
                        unit = temp[-1].split()[1]
                        temp[-1]=temp[-1].split()[0]
                        temp= map(float,temp)
                        if unit == "C":
                                temp=[t+units["C_K"] for t in temp]
                    else:
                        temp= map(float,temp)
                    delta= (temp[1] - temp[0])/md_total
                    temp_arra= np.arange(temp[0], temp[1], delta)
                    return temp_arra
                elif n_plat == 1:
                    temp= re.findall('\s*temp_plat\s+(.*)',data_file)[0].split(",")
                    if not temp[-1].replace('.','',1).isdigit(): # Unit is given
                        unit = temp[-1].split()[1]
                        temp[-1]=temp[-1].split()[0]
                        temp= map(float,temp)
                        if unit == "C":
                                temp=[t+units["C_K"] for t in temp]
                    else:
                        temp= map(float,temp)
        
                    step= re.findall('\s*temp_step\s+(.*)',data_file)[0].split(",")
                    if not step[-1].replace('.','',1).isdigit(): # Unit is given
                        unit = step[-1].split()[1]
                        step[-1]=step[-1].split()[0]
                        step= map(float,step)
                        if unit == "C":
                                step=[t+units["C_K"] for t in step]
                    else:
                        step= map(float,step)
        
                    for i, t in enumerate(temp):
                        if i == 0:
                            temp_arra= t*np.ones(step[i], dtype=float)
                        else:
                            temp_arra= np.concatenate((temp_arra,t*np.ones(step[i], dtype=float)),axis=0)
                    return temp_arra
            elif indicator == 2:
                print 'only one type of temperature control'
                temp_arra=[]
                return temp_arra
            elif indicator == 3:
                print 'only one type of temperature control'
                temp_arra=[]
                return temp_arra
        # Data
        self.s_t = None
        self.s_tdot = None
        self.p_t = None
        self.v_t = None
        self.h_t = None
        self.h_tdot = None
        self.x_t = None
        self.x_tdot = None

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class Structure:
    """
    Structure class
    """
    def __init__(self):
        self.lattice = None
        self.xred = None
        self.xcart = None
        self.fcart = None
        self.strten = None
        self.vel = None
        self.vel_h = None
        self.amu = None

# * * * * * * * * * * * * * * * * * * * * * * * * * * 

def run_md(md,constr,name,dft_code):
    """
    Run Molecular Dynamics
    """
    for i_dft_step in range(md.dft_steps):
        temp= temp_arra[i_dft_step*md.md_steps]
        print 'dft step  ', i_dft_step

        if i_dft_step == 0:
            #  First dft run. Take the prototype xxxx.in and xxxx.files
            #  and put them in what is going to be the working directory
            md.s_t=1.0       #thermostat degree of freedom
            md.s_tdot= 0.0  #time derivative of thermostat degree of freedom
            work_dir= name+str(i_dft_step)
            subprocess.call(['mkdir', work_dir],shell=True)
            ac.from_prototype_in_to_in_step0(name+'.in', work_dir+'/'+name+str(i_dft_step)+'.in')
            ac.from_prototype_file_to_file(name+'.files', work_dir+'/'+name+str(i_dft_step)+'.files', i_dft_step)
        else:
            work_dir= ac.create_directories(name, x_t, h_t, i_dft_step, pwd='.')
        rf= open(work_dir+'/'+name+str(i_dft_step)+'.files')
        log= open(work_dir+'/'+name+str(i_dft_step)+'.log','w')
        #        job= subprocess.Popen('mpirun -np 4 abinit', bufsize=1048576, shell=True, \
        #                              stdout=log, stdin=rf, cwd=work_dir)
        if input_para['np'] is not None:
            comand_string='mpirun -np %d abinit' % input_para['np'] 
            job= subprocess.Popen(comand_string, bufsize=1048576, shell=True,\
            stdout=log, stdin=rf, cwd=work_dir)
        else:
            job= subprocess.Popen('abinit', bufsize=1048576, shell=True,\
            stdout=log, stdin=rf, cwd=work_dir)
        n=0
        while job.poll() == None:
            #print job.poll()
            time.sleep(30)
            if os.path.exists(work_dir+'/'+name+str(i_dft_step)+'.out'):
                output= open(work_dir+'/'+name+str(i_dft_step)+'.out','r')
                data= output.read()
                match= re.search('Calculation\s+completed', data)
                if match and n == 0:
                    job.kill()
                    n=1
        #end if match and n == 0:
        #print job.poll()
        nat, mass, h_t, strten_in= \
        ac.get_nat_mass_latvec_in_strten_in(work_dir+'/'+name+str(i_dft_step)+'.out')
        x_t, f_t= ac.get_xred_fcart(work_dir+'/'+name+str(i_dft_step)+'.out', nat)
        #h_t_inv= np.linalg.inv(h_t)
        #F_redu_t= np.dot(h_t_inv, f_t)
        #out= md.md_npt_step(dt, md_steps, mass, Qmass, bmass, temp, correc_steps, x_t, x_t_dot, v_t, F_redu_t,\
        #            h_t, h_t_dot, strten_in, P_ext, s_t, s_t_dot)
        
        #---------------
        #   INIT VEL.
        #---------------
        if i_dft_step == 0:
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
            write_md_output(work_dir+'/'+name+str(i_dft_step)+'.mdout',\
                bond_const, angl_const, pressure_t, volu_t, bond_constrain_t, cos_constrain_t)
            for i,_ in enumerate(pressure_t):
                md_time= (i_dft_step*md_steps+i)*dt
                #pressure_volu_file.write('md_step     dft_step     total_step    time(fs)     pressure(hartree/Bohr^3)     volume(Bohr^3)\n')
                pressure_volu_file.write('%d          %d               %d             %.3f         %.3E                         %.3f\n'\
                %(i+1,i_dft_step+1,(i_dft_step*md_steps+i+1),md_time,pressure_t[i],volu_t[i]))
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

