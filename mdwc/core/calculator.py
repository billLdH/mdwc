#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import re
import numpy as np
import argparse
from mdwc.dft import *

class Calculator:
    def _init__(self,dft_code,input_para):
        self.dft_code = dft_code[0]
        self.dft_exec = dft_code[1]
        self.dft_opts = dft_code[2]
        self.calc_np = input_para["np"]
        self.calc_opts = input_para["mpi_options"]
        self.command = None

        if self.calc_np not None and
           self.calc_np > 1:
            self.command = "mpirun -np %s " % self.calc_np
            if self.calc_opts not None:
                self.command += "%s " % self.calc_opts
        else:
            self.command = ""

        self.command += "%s %s" % (self.dft_exec,self.dft_opts)

    def get_dft_code(self):
        return self.dft_code

    def get_dft_exec(self):
        return self.dft_exec

    def get_dft_opts(self):
        return self.dft_opts

    def get_calc_np(self):
        return self.calc_np

    def get_calc_opts(self):
        return self.calc_opts

    def get_command(self):
        return self.command

    def set_dft_code(self,dft_code):
        self.dft_code= dft_code

    def set_dft_exec(self,dft_exec):
        self.dft_exec= dft_exec

    def set_dft_opts(self,dft_opts):
        self.dft_opts= dft_opts

    def set_calc_np(self,calc_np):
        self.calc_np= calc_np

    def set_calc_opts(self,calc_opts):
        self.calc_opts= calc_opts

    def set_command(self,command):
        self.command= command

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
    """
    Create new directory and copy input files into this
    """

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def init_dft_dir():
