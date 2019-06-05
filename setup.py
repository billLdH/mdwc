#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function
import sys
import re
import setuptools
from numpy.distutils.core import Extension
from numpy.distutils.core import setup

# Check for python requirements
if sys.version_info[0] != 3:
    sys.stderr.write('Python 3.X is needed to use this package.\n')
    sys.exit(0)

try:
    import numpy
except ImportError:
    sys.stderr.write('Numpy package is needed to use this package.\n')
    sys.exit(0)

version = numpy.__version__.split(".")
if not all(int(item) >= 1 for item in version):
    sys.stderr.write('Numpy >= 1.1 1 is needed to use this package.\n')
    sys.exit(0)

# Program
scripts=['scripts/mdwc_']
packages=['libmdwc',
          'mdwc',
          'mdwc.core',
          'mdwc.dft',
          'mdwc.io',
          'mdwc.io.db',
          'mdwc.io.dft',
          'mdwc.io.md',
          'mdwc.postmdwc',
          'mdwc.utils']

wrapper = [Extension('libmdwc.parameters',
                    sources=['libmdwc/parameters.F90']),
           Extension('mdwc.libmdwc.maths',
                    sources=['libmdwc/parameters.F90',
                             'libmdwc/maths.F90']),
            Extension('libmdwc.libmdwc',
                    sources=['libmdwc/parameters.F90',
                             'libmdwc/maths.F90',
                             'libmdwc/libmdwc.F90'])]

# Add informations
lines= open("PACKAGE_INFO.txt").readlines()
info= dict()
for line in lines:
    split = re.split('[=\n]',line)
    split = [s.replace('"','') for s in split]
    info[str(split[0])] = str(split[1])

# Setup
setup(
    name=info["__name__"],
    version=info["__version__"],
    license=info["__license__"],
    author=info["__author__"],
    maintainer=info["__maintainer__"],
    maintainer_email=info["__maintainer_email__"],
    description=info["__description__"],
    url=info["__url__"],
    download_url=info["__download_url__"],
    packages=packages,
    ext_modules=wrapper,
    scripts=scripts
)
