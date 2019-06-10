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
from mdwc.core.molecular_dynamics import md_nvt_constrains, md_npt_constrains
from mdwc.dft import *
from libmdwc.libmdwc import *

class MD:
    """
    Molecular Dynamics class
    """
    def __init__(self,name,wkdir):
        self.mdfile= wkdir+"/"+name+".md"
        # Input MD parameters
        self.mdInput= readMDIn(self.mdfile)
        self.mdtype = self.mdInput["mdtype"]
        check_md_type(self.mdtype)
        self.mdstep = self.mdInput["mdstep"]
        self.dftstep = self.mdInput["dftstep"]
        self.qmass = self.mdInput["qmass"]
        self.bmass = self.mdInput["bmass"]
        self.dt = self.mdInput["dt"]
        self.pressure = self.mdInput["pressure"]
        self.correct_spteps = self.mdInput["correct_spteps"]
        self.md_steps = self.mdInput["md_steps"]
        self.dft_steps = self.mdInput["dft_steps"]
        self.total_steps = mdInput["md_steps"]*mdInput["dft_steps"]
        self.temp = self.mdInput["temp"]

        Constraints.__init__(self,self.mdInput)

    def get_mdfile(self):
        return self.mdfile

    def get_mdtype(self):
        return self.mdtype

    def get_mdstep(self):
        return self.mdstep

    def get_md_steps(self):
        return self.md_steps

    def get_dft_steps(self):
        return self.dft_steps

    def get_total_steps(self):
        return self.total_steps

    def get_temp(self):
        return self.temp

    def get_dftstep(self):
        return self.dftstep
    
    def get_bmass(self):
        return self.bmass

    def get_qmass(self):
        return self.qmass

    def get_dt(self):
        return self.dt

    def get_pressure(self):
        return self.pressure

    def get_correct_spteps(self):
        return self.correct_spteps

    def set_bmass(self,bmass):
        self.bmass = bmass

    def set_qmass(self,qmass):
        self.qmass = qmass

    def set_mdfile(self,mdfile):
        self.mdfile = mdfile

    def set_mdtype(self,mdtype):
        self.mdtype = mdtype

    def set_mdstep(self,mdstep):
        self.mdstep = mdstep

    def set_md_steps(self,md_steps):
        self.md_steps = md_steps

    def set_dftstep(self,dftstep):
        self.dftstep = dftstep

    def set_dft_steps(self,dft_steps):
        self.dft_steps = dft_steps

    def set_dt(self,dt):
        self.dt = dt

    def set_pressure(self,pressure):
        self.pressure = pressure

    def set_correct_spteps(self,correct_spteps):
        self.correct_spteps = correct_spteps

    def set_total_steps(self,total_steps):
        self.total_steps = total_steps

    def set_temp(self,temp):
        self.temp = temp

    def get_md_parameters(self):
        """
        DEPRECATED !!!! SHOULD BE REMOVED ONCE THE MD SPARER IS CREATED
        """
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
    
        data.close()
    
    def temp_data_reader(self):
        """
        DEPRECATED !!!! SHOULD BE REMOVED ONCE THE MD SPARER IS CREATED
        """
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
        self.f_t = None

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def run_md(calc,md,constr,name,dft_code,datafile):
    """
    Run Molecular Dynamics
    """
    md_time = time.clock()

    for i_dft_step in range(md.dft_steps):

        md.dftstep = i_dft_step

        # Time
        dft_time= time.clock()
        temp= temp_arra[i_dft_step*md.md_steps]
        print('dft step  ', i_dft_step)

        # Specific to Abinit (an interface should be called) 
        #  1) init_dft_dir whatever the dft_step is
        #  2) if == 0 or != 0, modify input files
        if i_dft_step == 0:
            #  First dft run. Take the prototype xxxx.in and xxxx.files
            #  and put them in what is going to be the working directory
            md.s_t=1.0       #thermostat degree of freedom
            md.s_tdot= 0.0  #time derivative of thermostat degree of freedom
            work_dir= name+str(i_dft_step)
            subprocess.call('mkdir %s' work_dir,shell=True)
            # Specific to Abinit (an interface should be called) ==> init_dft_dir
            from_prototype_in_to_in_step0(name+'.in', work_dir+'/'+name+str(i_dft_step)+'.in')
            from_prototype_file_to_file(name+'.files', work_dir+'/'+name+str(i_dft_step)+'.files', i_dft_step)
        else:
            work_dir= create_directories(name, x_t, h_t, i_dft_step, pwd='.')

        # Specific to Abinit (an interface should be called)
        rf= open(work_dir+'/'+name+str(i_dft_step)+'.files')
        log= open(work_dir+'/'+name+str(i_dft_step)+'.log','w')

        #-----------
        #   RUN !
        #-----------
        job= subprocess.Popen(calc.command, bufsize=1048576, shell=True,\
        stdout=log, stdin=rf, cwd=work_dir)
        job.wait()

            # Specific to Abinit (an interface should be called to check endding of run)
            if os.path.exists(work_dir+'/'+name+str(i_dft_step)+'.out'):
                output= open(work_dir+'/'+name+str(i_dft_step)+'.out','r')
                data= output.read()
                match= re.search('Calculation\s+completed', data)
                if match and n == 0:
                    job.kill()
                    n=1
        #end if match and n == 0:
        #print job.poll()
        nat, mass, md.h_t, strten_in= \
        ac.get_nat_mass_latvec_in_strten_in(work_dir+'/'+name+str(i_dft_step)+'.out')
        md.x_t, md.f_t= ac.get_xred_fcart(work_dir+'/'+name+str(i_dft_step)+'.out', nat)
        #h_t_inv= np.linalg.inv(h_t)
        #F_redu_t= np.dot(h_t_inv, f_t)
        #out= md.md_npt_step(dt, md_steps, mass, Qmass, bmass, temp, correc_steps, x_t, x_t_dot, v_t, F_redu_t,\
        #            h_t, h_t_dot, strten_in, P_ext, s_t, s_t_dot)
        
        #---------------
        #   INIT VEL.
        #---------------
        if i_dft_step == 0:
            # Initialization of velocities
            md.v_t= init_vel_atoms(mass, md.temp, len(mass))
            md.h_tdot= init_vel_lattice(bmass, md.temp, md.h_t)
            md.x_tdot= get_x_dot(md.h_t, md.v_t, nat)
            
        #--------------
        #   RUN  NPT
        #--------------
        if md.mdtype == "npt":
            md.s_t, md.s_tdot, md.p_t, md.v_t,\
            bond_constrain_t, cos_constrain_t, md.h_t,\
            md.h_tdot, md.x_t, md.x_tdot, md.v_t= \
                md_npt_constrains(md.h_t,md.x_t, \
                    md.x_tdot, md.f_t, strten_in,md.v_t,md.h_tdot,\
                    bond_valu, angl_valu, cell_para_valu,\
                    cell_angl_valu, volu_valu, atom_fix_valu,atom_fix_cord,\
                    md.pressure,mass,\
                    md.qmass, md.bmass, md.dt, md.temp, md.s_t, md.s_tdot, \
                    bond_const,angl_const, cell_para_const,\
                    cell_angl_const, atom_fix_const,correc_steps, md_steps,\
                    bool_bond_cons,bool_angl_cons,\
                    bool_cell_para_cons,bool_cell_angl_cons,\
                    bool_volu,bool_atom_fix_cons,volu_cons, nat, \
                    numb_cell_angl_cons,numb_cell_para_cons,\
                    numb_angl_cons, numb_bond_cons,numb_atom_fix_cons)    
        elif md.mdtype == "nvt":
            #--------------
            #   RUN  NVT
            #--------------
            md.s_t, md.s_tdot, md.x_t, md.v_t= md_nvt_constrains(md.h_t,md.x_t, \
                    md.f_t,md.v_t,\
                    bond_valu, angl_valu,\
                    atom_fix_valu,atom_fix_cord,mass,\
                    md.qmass, md.dt, md.temp, md.s_t, md.s_tdot,\
                    bond_const,angl_const,\
                    atom_fix_const,correc_steps, md_steps,\
                    bool_bond_cons,bool_angl_cons,\
                    bool_atom_fix_cons, nat,\
                    numb_angl_cons, numb_bond_cons,numb_atom_fix_cons)

        # Common output files
        write_md_output(work_dir+'/'+name+str(i_dft_step)+'.mdout',\
            bond_const, angl_const, pressure_t, volu_t, bond_constrain_t, cos_constrain_t)
        for i,_ in enumerate(pressure_t):
            md_time= (i_dft_step*md_steps+i)*dt
            pressure_volu_file.write('%d          %d               %d             %.3f         %.3E                         %.3f\n'\
            %(i+1,i_dft_step+1,(i_dft_step*md_steps+i+1),md_time,pressure_t[i],volu_t[i]))

        print("MD step duration: ",str(datetime.timedelta(time.clock() - dft_time))
    print("MD duration: ",str(datetime.timedelta(time.clock() - md_time))
