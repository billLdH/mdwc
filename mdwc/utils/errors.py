#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

def _error(message,code):
    """
    Print error message and exit
    """
    print("< x > ERROR\n "+message)
    exit(code)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

def _warning(message):
    """
    Print warning message
    """
    print("< ! > WARNING\n "+message)

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class NotImplemented(Exception):
    pass

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class NameError(Exception):
    pass

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class InputError(Exception):
    pass

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class ValueError(Exception):
    pass

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class SCFError(Exception):
    pass

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class CalculationStopped(Exception):
    pass

