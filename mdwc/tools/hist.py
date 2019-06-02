#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os

# Not yet implemented
#
# Objectives for this module: 
#       Store libraries which allow to manage MD history.
#       Usefull for post-treatment analysis, restart, help,...
#       The main script should be located into the scripts directory.
#
# Requirements:
#       Database file (YAML, XML, CSV, JSON, NetCDF)
#
# Ideas:
#   - Create an averaged structure (following to the DFT code choice) 
#     based on a window of:
#       1) Steps: [Step_ini, Step_end] 
#       2) Temperature (usefull if plateaus): [T, Delta_T] or [T_ini, T_end]
#       3) Pressure: [P, Delta_P] or [P_ini, P_end]
#       4) Volume: [V, Delta_V] or [V_ini, V_end]
#
#   - MD analysis:
#       1) Atomic position
#       2) Cell
#       3) ...
#
#   - Visualization:
#       1) Plot data (using Matplotlib,...)
#       2) MD Live (using Mayavi,...)
#
#   - Interactive manager to create file.md
