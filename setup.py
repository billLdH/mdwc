#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function
import sys
from setuptools import setup
from numpy.distutils.core import Extension
# from numpy.distutils.core import setup

# Check for python requirements
if sys.version_info[0] /= 3:
    sys.stderr.write('Python 3.X is needed to use this package.\n')
    sys.exit(0)

if 'numpy' not in sys.modules:
    sys.stderr.write('Numpy package is needed to use this package.\n')
    sys.exit(0)
else:
    version = numpy.__version__.split(".")
    if not all(int(item) >= 1 for item in version):
        sys.stderr.write('Numpy >= 1.1 1 is needed to use this package.\n')
        sys.exit(0)

# Informations
__name__="mdwc"
__version__ =0.2.0
__author__ = "Aldo H. Romero, Arturo Hernandez, Uthpala Herath, Pedram Tavazohi"
# __licence__ = ""  <----- TO BE SET
__maintainer__ ="Aldo H. Romero"
__maintainer_email__ ="Aldo.Romero@mail.wvu.edu"
__description__="Molecular Dynamics With Constraints"
__date__ = "June 2019"
__url__="https://molecular-dynamics-with-constraints.github.io/"
__download_url__="https://github.com/romerogroup/mdwc.git"

# Program
scripts=['scripts/mdwc_']
packages=['dft_interfaces',
          'libmdwc',
          'manager',
          'tools']
ext_modules=[Extension('libmdwc.libmdwc',
                       ['libmdwc/libmdwc.F90']),
             Extension('libmdwc.parameters',
                       ['libmdwc/parameters.F90'])]

# Setup
setup(
    name=__name__,
    version=__version__,
    author=__author__,
    maintainer=__maintainer__,
    maintainer_email=__maintainer_email__,
    description=__description__,
    url=__url__,
    download_url=__download_url__,
    packages=packages,
    ext_modules=ext_modules,
    scripts=scripts
)
