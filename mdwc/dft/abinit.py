#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import subprocess
import time
import re
import os.path
import numpy as np


class Abinit:
    def __init__(self,finput,ffiles,foutput):

    def read_input(self,filename):
        if not os.path.isfile(filename):
            _error("Abinit input file "+ filename+ " is missing.",0)
        self.input = readAbinitIn(filename)

    def init_from_file(self):
        self.input= AbinitInputFiles(files)

    

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_abinit_files(name):
    """
    Check if the following files exist:
        - name.in
        - name.files
    """
    abi_files=[file for file in os.listdir(".") if file.endswith('.in','files')]
    if name+".in" or name+".files" not in abi_files:
        _error("Check name of Abinit files. Set '-n [NAME]' according to.",0)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_nat_mass_latvec_in_strten_in(path_to_file):
    data= open(path_to_file).read()
    nat= int(re.findall('natom\s+([0-9]+)', data)[0])
    typat_str_0= '\s+typat\s+'
    typat_srt_1='.+'
    typat_str=typat_str_0+'('+typat_srt_1+')'
    typat= map(int, re.findall(typat_str,data)[0].split())
    #znucl= map(float, re.findall('\s+znucl((?:\s+\d+.\d+\s+)+)',data))
    znucl= map(int, map(float, re.findall('\s+znucl\s+(.+)',data)[0].split()))
    while len(typat) < nat:
        typat_srt_1= typat_srt_1+'\n.+'
        typat_str=typat_str_0+'('+typat_srt_1+')'
        #x= re.findall('\s+typat\s+(.+)',data)
        #print x
        typat= map(int, re.findall(typat_str,data)[0].split())
    mass=[]
    for i in typat:
        mass.append(masses[znucl[i-1]])
    mass= np.array(mass)
    a1= map(float, re.findall('R.1.=\s*(.\d+...\d+\s+.\d+...\d+\s+.\d+...\d+)', data)[0].split())
    a2= map(float, re.findall('R.2.=\s*(.\d+...\d+\s+.\d+...\d+\s+.\d+...\d+)', data)[0].split())
    a3= map(float, re.findall('R.3.=\s*(.\d+...\d+\s+.\d+...\d+\s+.\d+...\d+)', data)[0].split())
    latvec_in= np.array([a1,a2,a3]).T
    latvec_in.astype('float64')
    strten_in= []
    strten_in.append(np.float64(re.findall('sigma.1\s+1.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in.append(np.float64(re.findall('sigma.2\s+2.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in.append(np.float64(re.findall('sigma.3\s+3.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in.append(np.float64(re.findall('sigma.3\s+2.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in.append(np.float64(re.findall('sigma.3\s+1.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in.append(np.float64(re.findall('sigma.2\s+1.=(\s+.\d+.\d+..\d+)', data)[0]))
    strten_in= np.array(strten_in)
    return nat, mass, latvec_in, strten_in

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_xred_fcart(path_to_file, nat):
    #1 Ha/Bohr3 = 29421.02648438959 GPa
    data= open(path_to_file).readlines()
    for n,line in enumerate(data):
        if re.findall('reduced\s+coordinates\s+.array\s+xred', str(line)): 
            xred_temp=  data[n+1:n+1+nat]
            xred= np.array([map(float, i.split('\n')[0].split()) for i in xred_temp]).T
            xred.astype('float64')
        elif re.findall('cartesian\s+forces\s+.hartree.bohr', str(line)): 
            fcart_temp=  data[n+1:n+1+nat]
            fcart= np.array([map(float, i.split('\n')[0].split()) for i in fcart_temp])[:,1:]
            fcart= fcart.T
            fcart.astype('float64')
        elif re.findall('>>>>>>>>>\s+Etotal=\s+.\d+', str(line)):#hartree 
            ener=  re.findall('>>>>>>>>>\s+Etotal=(\s+.\d+.\d+..\d+)', str(line))
            ener= np.float64(ener[0])
        elif re.findall('Pressure=\s+\d+.\d+..\d+', str(line)):#this preassure in GPa
            pressure=  re.findall('Pressure=(\s+\d+.\d+..\d+)', str(line))
            pressure= np.float64(pressure[0])
    return xred, fcart

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_out_exit_and_complet(path_to_output):
	if os.path.exists(path_to_output):
		#time.sleep(30)
		output= open(path_to_output,'r')
		data= output.read()
		match= re.search('Calculation\s+completed', data)
		if match:
			output.close()
			n=1
			return n
		output.close()
		time.sleep(30)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def create_directories(name, xred, h, numb, pwd= None):
    if pwd == None:
        pwd= subprocess.check_output(['pwd'])
    new_dir= pwd+'/'+name+str(numb)
    subprocess.check_call(['mkdir', new_dir])
    path_to_prot_in= pwd+'/'+name+'.in'
    path_to_prot_files= pwd+'/'+name+'.files'
    path_to_new_in= new_dir+'/'+name+str(numb)+'.in'
    path_to_new_files= new_dir+'/'+name+str(numb)+'.files'
    from_prototype_in_to_in(path_to_prot_in, path_to_new_in, xred, h)
    from_prototype_file_to_file(path_to_prot_files, path_to_new_files, numb)
    return new_dir

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def from_prototype_in_to_in_step0(path_to_prot_in, path_to_new_in):
    #get in from prototipe in
    data_prot= open(path_to_prot_in).readlines()
    data_new=  open(path_to_new_in,'w')

    for n,line in enumerate(data_prot):
		data_new.write(line)       
    data_new.close()
    return None

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def from_prototype_in_to_in(path_to_prot_in, path_to_new_in, xred, h):
    #get in from prototipe in
    pattern1 = re.compile("^[a-z]")
    pattern2 = re.compile("^#")
    data_prot= open(path_to_prot_in).readlines()
    data_new=  open(path_to_new_in,'w')
    a1= np.linalg.norm(h[:,0])
    a2= np.linalg.norm(h[:,1])
    a3= np.linalg.norm(h[:,2])
    a1v= np.divide(h[:,0],a1)
    a2v= np.divide(h[:,1],a2)
    a3v= np.divide(h[:,2],a3)

    for n,line in enumerate(data_prot):
        if pattern1.match(line) or pattern2.match(line):
            if re.findall('\s*acell', str(line)):
                string='acell %0.5f %0.5f %0.5f\n' \
                % (a1, a2, a3)
                data_new.write(string)

            elif re.findall('\s*rprim', str(line)):
                string= 'rprim   %0.5f %0.5f %0.5f\n'% (a1v[0], a2v[0], a3v[0])
                for i in range(2): 
                    string= string+'        %0.5f %0.5f %0.5f\n'%(a1v[i+1], a2v[i+1], a3v[i+1])
                data_new.write(string)
            elif re.findall('\s*xred', str(line)):
                string='xred   \n'
                for red_coor in xred.T:
                    string= string+'%0.5f %0.5f %0.5f\n' % (red_coor[0],red_coor[1],red_coor[2])
                data_new.write(string)
            else:
                data_new.write(line)       
    data_new.close()
    return None

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def from_prototype_file_to_file(path_to_prot_files, path_to_new_files, numb):
    data_prot= open(path_to_prot_files).readlines()
    data_new=  open(path_to_new_files,'w')
    for n,line in enumerate(data_prot):
	data_new.write(line.replace("*",str(numb)))
    data_new.close()
    return None    
