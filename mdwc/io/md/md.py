#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import re
import sys

def readMDIn(filename):

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def ParserMD(mdfile):
    data = open(mdfile).readlines()
    tags = [line.split()[0] for line in data]
    tags = [tags.remove(tag) for tag in tags if "#" in tag]
