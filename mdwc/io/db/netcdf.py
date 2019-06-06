#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from __future__ import division, print_function

import sys
import os
import netCDF4

class NetCDF:
    def __init__(self,ncfile,dft_code):
        self.ncfile = ncfile
        self.dft_code = dft_code

    def write(self):
        # Dataset
        nc_dtset = Dataset(ncfile,"w",format="NETCDF4")

        # Global Attributes
        nc_dtset.setncattr("file_format","NETCDF4")
        nc_dtset.setncattr("Conventions","http://www.etsf.eu/fileformats/")
        nc_dtset.setncattr("code",self.dft_code)

        # Dimensions
        nc_dtset.createDimension("time",None)
        nc_dtset.createDimension("xyz",3)
        nc_dtset.createDimension("ntypat",ntypat.size)
        nc_dtset.createDimension("natom",natom.size)
        nc_dtset.createDimension("two",two.size)
        nc_dtset.createDimension("six",six.size)
        nc_dtset.createDimension("npsp",npsp.size)

        # Variables
        mdtime_var = nc_dtset.createVariable('mdtime','double',('time'))
        mdtime_var[:] =
        mdtime_var.units = "hbar/Ha"
        mdtime_var.mnemonics = "Molecular Dynamics or Relaxation TIME"

        acell_var = nc_dtset.createVariable('acell','double',('time','xyz'))
        acell_var.units = "bohr"
        acell_var.mnemonics = "CELL lattice vector scaling"

        acell_var = nc_dtset.createVariable('rec_cell','double',('time','xyz'))
        acell_var.units = ""
        acell_var.mnemonics = "RECiprocal CELL lattice vector scaling"

        amu_var = nc_dtset.createVariable('amu','double',('ntypat'))
        amu_var[:] = amu[:]
        amu_var.units = "atomic units"
        amu_var.mnemonics = "atomic masses"

        dt_var = nc_dtset.createVariable('dt','double')
        dt_var[:] = 1.
        dt_var.units = "atomic units"
        dt_var.mnemonics = "time step"

        ekin_var = nc_dtset.createVariable('ekin','double',('time'))
        ekin_var.units = "Ha"
        ekin_var.mnemonics = "Energy KINetic ionic"

        entropy_var = nc_dtset.createVariable('entropy','double',('time'))
        entropy_var.units = ""
        entropy_var.mnemonics = "Entropy"

        etotal_var = nc_dtset.createVariable('etotal','double',('time'))
        etotal_var.units = "Ha"
        etotal_var.mnemonics = "TOTAL Energy"

        fcart_var = nc_dtset.createVariable('fcart','double',('time','natom','xyz'))
        fcart_var.units = "Ha/bohr"
        fcart_var.mnemonics = "atom Forces in CARTesian coordinates"

        fred_var = nc_dtset.createVariable('fred','double',('time','natom','xyz'))
        fred_var.units = "dimensionless"
        fred_var.mnemonics = "atom Forces in REDuced coordinates"

        mdtemp_var = nc_dtset.createVariable('mdtemp','double',('two'))
        mdtemp_var[:] = np.array([100., 100.])
        mdtemp_var.units = "Kelvin"
        mdtemp_var.mnemonics = "Molecular Dynamics Thermostat Temperatures"

        rprimd_var = nc_dtset.createVariable('rprimd','double',('time','xyz','xyz'))
        rprimd_var.units = "bohr"
        rprimd_var.mnemonics = "Real space PRIMitive translations, Dimensional"

        strten_var = nc_dtset.createVariable('strten','double',('time','six'))
        strten_var.units = "Ha/bohr^3"
        strten_var.mnemonics = "STRess tensor"

        typat_var = nc_dtset.createVariable('typat','double',('natom'))
        typat_var[:] = typat[:]
        typat_var.units = "dimensionless"
        typat_var.mnemonics = "types of atoms"

        vel_var = nc_dtset.createVariable('vel','double',('time','natom','xyz'))
        vel_var.units = "bohr*Ha/hbar"
        vel_var.mnemonics = "VELocities of atoms"

        vel_cell_var = nc_dtset.createVariable('vel_cell','double',('time','xyz','xyz'))
        vel_cell_var.units = "bohr*Ha/hbar"
        vel_cell_var.mnemonics = "VELocities of CELL"

        xcart_var = nc_dtset.createVariable('xcart','double',('time','natom','xyz'))
        xcart_var.units = "bohr"
        xcart_var.mnemonics = "vectors (X) of atom positions in CARTesian coordinates"

        xred_var = nc_dtset.createVariable('xred','double',('time','natom','xyz'))
        xred_var.units = "dimensionless"
        xred_var.mnemonics = "vectors (X) of atom positions in REDuced coordinates"

        znucl_var = nc_dtset.createVariable('znucl','double',('npsp'))
        znucl_var.units = "atomic units"
        znucl_var.mnemonics = "atomic charges"
        znucl_var[:] = znucl[:]

        nc_dtset.close()

    def read(self):
        # Dataset
        nc_dtset = Dataset(ncfile,"r",format="NETCDF4")

        # Dimensions
        ntypat = nc_dtset.dimensions["ntypat"]
        natom = nc_dtset.dimensions["natom"]
        npsp = nc_dtset.dimensions["npsp"]
        time = nc_dtset.dimensions["time"]

        # Variables
        # Store in a dictionary ?
        self.mdtime = nc_dtset.variables["mdtime"][:]
        self.acell = nc_dtset.variables["acell"][:]
        self.rec_cell = nc_dtset.variables["rec_cell"][:]
        self.amu = nc_dtset.variables["amu"][:]
        self.dt = nc_dtset.variables["dt"][:]
        self.ekin = nc_dtset.variables["ekin"][:]
        self.entropy = nc_dtset.variables["entropy"][:]
        self.etotal = nc_dtset.variables["etotal"][:]
        self.fcart = nc_dtset.variables["fcart"][:]
        self.fred = nc_dtset.variables["fred"][:]
        self.mdtemp = nc_dtset.variables["mdtemp"][:]
        self.rprimd = nc_dtset.variables["rprimd"][:]
        self.strten = nc_dtset.variables["strten"][:]
        self.typat = nc_dtset.variables["typat"][:]
        self.vel = nc_dtset.variables["vel"][:]
        self.vel_cell = nc_dtset.variables["vel_cell"][:]
        self.xcart = nc_dtset.variables["xcart"][:]
        self.xred = nc_dtset.variables["xred"][:]
        self.znucl = nc_dtset.variables["znucl"][:]
        
        # Close
        nc_dtset.close()
