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

def quick_check():
    """
    Check options and if file.md exists
    DEPRECATED !!!!!! EVERYTHING IS INTO THE MD FILE
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

def check_filename():
    """
    Check if filename is set and return it
    """

    # MD file
    mdfiles = [file for file in os.listdir(".") if file.endswith('.md')]
    if len(mdfiles) > 2:
        _error("File.md is non-unique.",0)
    elif len(mdfiles) < 1:
        _error("File.md does not exist in the directory.",0)
    else:
        name= str(mdfiles[0])
    return name

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_md_type(mdtype):
    """
    Check if MD type is set and return it
    """
    # MD type
    if mdtype in ["NPT","npt"]:
        return "npt"
    elif mdtype in ["NVT","nvt"]:
        return "nvt"
    else:
        _error("MD type is not set correctly.",0)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_dft_code(mdInput):
    """
    Check if DFT code is correctly set as well as the existence of the executable
    """

    # Absolute path to a pecific executable of the DFT code
    exec_dft = mdInput["exec_dft"]
    if exec_dft is None:
        # binary in PATH
        exec_dft= dft_code

    if shutil.which(exec_dft) is None:
        _error("Executable of the DFT code does not exist.",0)

    # DFT Code options
    opt_dft= mdInput["opt_dft"]

    return dft_code,exec_dft,opt_dft

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_db_packages(db_fmt):
    """
    Check if a MD database can be created.
    """
    packages = ['xml',
                'yaml',
                'netCDF4',
                'csv',
                'json']

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

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def check_succeed(output,words):
    if os.path.exists(output):
        return str(words) in open(output).read():
    else:
        _error("Output not find. Error in the path.",0)
