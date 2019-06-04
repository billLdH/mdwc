#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import subprocess
import time
import re
import os.path
import numpy as np

def check_succeed(output,words):
    if os.path.exists(output):
        return str(words) in open(output).read():
    else:
        _error("Output not find. Error in the path.",0)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def create_dirs(name, xred, h, step, pwd= None):
    directory = name+str(step)
    subprocess.call('mkdir %s' % directory, shell=True)
    [subprocess.call('cp %s %s/' % (fin,directory)) for fin in inputs]

# * * * * * * * * * * * * * * * * * * * * * * * * * *
    
def copy_inputs(inputs,directory):
    [subprocess.call('cp %s %s' % (fin,directory)) for fin in inputs]
