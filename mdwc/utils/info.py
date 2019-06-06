#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function
import re

class Info:
    def __init__(self,info_file):
        self.lines= open(info_file).readlines()
        info= dict()
        for line in lines:
            split = re.split('[=\n]',line)
            split = [s.replace('"','') for s in split]
            info[str(split[0])] = str(split[1])

        self.__name__=info["__name__"]
        self.__version__ =info["__version__"]
        self.__license__ = info["__license__"]
        self.__author__ = info["__author__"]
        self.__maintainer__ = info["__maintainer__"]
        self.__university__ = info["__university__"]
        self.__maintainer_email__ = info["__maintainer_email__"]
        self.__description__=info["__description__"]
        self.__date__ = info["__date__"]
        self.__url__= info["__url__"]
        self.__download_url__=info["__download_url__"]

    def get_name(self):
        self.__name__

    def get_version(self):
        self.__version__

    def get_license(self):
        self.__license__

    def get_author(self):
        self.__author__

    def get_maintainer(self):
        self.__maintainer__

    def get_university(self):
        self.__university__

    def get_maintainer_email(self):
        self.__maintainer_email__

    def get_description(self):
        self.__description__

    def get_date(self):
        self.__name__

    def get_name(self):
        self.__name__

    def get_url(self):
        self.__url__

    def get_download_url(self):
        self.__download_url__

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_system_info():
    """
    Print informations on the current system
    """
    print("""
 < i > System informations
 System:       %s
 Release:      %s
 Machine:      %s
 Processor:    %s
 Architecture: %s
    """ % (platform.system(),
           platform.release(),
           platform.machine(),
           platform.processor(),
           platform.architecture()[0]))

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def get_python_info():
    """
    Print informations on the python tool
    """
    print("""
 < i > Python informations
 Version:        %s
 Compiler:       %s
 Implementation: %s
    """ % (platform.python_version(),
           platform.python_compiler(),
           platform.python_implementation())
