#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import sys

def readMDIn(filename):
    """
    Read MD files
    """
    lines = open(mdfile).readlines()

    # Clean comments
    tags = [line.split()[0] for line in lines]
    lines = [lines.remove(line) for n,line in enumerate(lines) if str(tags[n][0]) == "#"]
    tags = [line.split()[0] for line in lines]
    # Get Data
    # Save in dict
    # mdInput = { Qmass: [qmass,unit],
    #             Bmass: [bmass,unit],
    #             temp:  [np.array([temp_1,temp_2]),unit],
    #             ... }
    mdInput = dict()
    for l,line in enumerat(lines):
        key,value= ParserMD(tags[l],line)
        dict[str(key)] = value

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def ParserMD(mdfile):
    """
    MD parser
    """
    # Use findall as in get_md_parameters or get_constrains_values
    # Need to be generalized to read arrays and units
    # A list containing [bmass,unit] or [np.array([temp_1,temp_2]),unit] as to be returned
    # get_md_parameters and get_constrains_values should be removed after
