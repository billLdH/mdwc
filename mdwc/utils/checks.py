#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function
import sys

def check_python_env():
    """
    Check for python requirements
    """
    if sys.version_info[0] != 3:
        _error('Python 3.X is needed to use this package.\n',0)
    
    try:
        import numpy
    except ImportError:
        _error('Numpy package is needed to use this package.\n',0)
    
    version = numpy.__version__.split(".")
    if not all(int(item) >= 1 for item in version):
        _error('Numpy >= 1.1 1 is needed to use this package.\n',0)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def quick_check():
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

def check_filename(input_para):
    """
    Check if filename is set and return it
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
    return name

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_md_type(input_para,mdfile):
    """
    Check if MD type is set and return it
    """
        # MD type
    if input_para["npt"] is None and input_para["nvt"] is None:
        mdtype= [str(re.findall('\s*MD\s+(.*)',line)[0].split()[0]) \
                 for line in open(mdfile).readlines() if re.match('MD')]
        if len(mdtype) != 0:
            _error("MD type is not set correctly.",0)
        else:
            if mdtype[0] in ["NPT","npt"]:
                return "npt"
            elif mdtype[0] in ["NVT","nvt"]:
                return "nvt"
            else:
                _error("MD type is not set correctly.",0)
    elif input_para["npt"] is not None and input_para["nvt"] is not None
        _error("MD type is not set correctly.",0)
    elif input_para["npt"] is not None:
        return "npt"
    elif input_para["nvt"] is not None:
        return "nvt"

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_dft_code(mdfile,name):
    """
    Check if DFT code is correctly set as well as the existence of the executable
    """
    # DFT Code
    data= open(mdfile).readlines()
    dft_code = interface.get_dft_code(data,mdfile,name)

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

    # DFT Code options
    opt_dft = [str(re.findall('\s*opt_dft_code\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('opt_dft_code')]

    return [dft_code,exec_dft,opt_dft]

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_db_packages(mdfile):
    """
    Check if a MD database can be created.
    """
    packages = ['xml',
                'yaml',
                'netCDF4',
                'csv',
                'json']

    data= open(mdfile).readlines()
    db_fmt = [str(re.findall('\s*db_fmt\s+(.*)',line)[0].split()[0]) \
                 for line in data if re.match('db_fmt')]

    if db_fmt in ["XML","xml"]:
        db_fmt= "xml"
        pkg= "xml"
    elif db_fmt in ["YAML","yaml"]:
        db_fmt= "yaml"
        pkg= "yaml"
    elif db_fmt in ["NETCDF","netCDF","NetCDF","netcdf"]:
        db_fmt= "netcdf"
        pkg= "NetCDF4"
    elif db_fmt in ["CSV","csv"]:
        db_fmt= "csv"
        pkg= "csv"
    elif db_fmt in ["JSON","json"]:
        db_fmt= "json"
        pkg= "json"

    try:
        import pkg
    except ImportError:
        _error(pkg+" package not installed.",0)

    return db_fmt
