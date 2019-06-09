#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import sys

class AbinitInputFiles(AbiInput,AbiFiles):
    def __init__(self,structure,files):
        self.input= readIn(structure,files[0])
        self.files= readFiles(structure,files[1])

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class AbinitOutputFiles(AbiOutput):
    def __init__(self,structure,files):
        self.output= readOut(structure,files[0])

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class AbiInput(dict):
    """
    Abinit Input object consisting of a dictionary
    """
    def __init__(self,structure,filename):
        # Structure object
        self.structure = structure
        data= open(filename,"r").read()
    
    def __str__(self):
        # Store input file as a string

    def readIn(self,filename):
        # Store everything in a dict
        AbinitParser

    def writeIn(self,filename):

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def AbinitParser(line):

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class AbiFiles(dict):
    def readFiles(self,filename):

    def writeFiles(self,filename):

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class AbiOutput(dict):
    def __init__(self,ffiles):
        self.ffiles = ffiles

    def readOut(self,filename):

