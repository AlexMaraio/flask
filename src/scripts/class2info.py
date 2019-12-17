#! /usr/bin/env python

"""
USAGE:   ini2info.dat <CLASS_INPUT> <FIELDS_INFO_FILE>
EXAMPLE: ini2info.dat prec17_20_dens.ini prec17_20_dens/fields-info.dat

This script takes a CLASS input file and creates a file used by 
FLASK describing the simulated fields and redshift bins (basically a 
table of field and redshift bin IDs, mean values, shift parameters and 
redshift ranges).

There are three methods for computing the shift parameter for convergence:
A table read from a file which is interpolated, the formula from 
Hilbert, Hartlap & Schneider (2011), and a formula computed from FLASK 
density line of sight integration. The latter is currently used (the other 
ones are commented).

Written by: Henrique S. Xavier, hsxavier@if.usp.br, 08/jul/2015.
"""

from __future__ import division, print_function
import sys
import numpy as np

# Docstring output:
if len(sys.argv) != 1 + 2: 
    print(__doc__)
    sys.exit(1)


# Internal definitions:
GalMean    = 0.0
KappaMean  = 0.0
GalShift   = 1.0
FixKappa   = 0
KappaShift = 1.0
GalType    = 1
KappaType  = 2
#shiftfile  = "/home/skems/pkphotoz/prog/corrlnfields/data/Hilbert2011_shifts.dat"
#shiftfile  = "/home/skems/pkphotoz/prog/corrlnfields/data/k0_empty_LCDM_Om30.dat"

# Load shift file:
# ATTENTION!! Values not extrapolated: extremes are used!
#fileZ, fileSh = np.loadtxt(shiftfile, unpack=True)


# Get input:
classinput = sys.argv[1]
fieldinfo  = sys.argv[2]

# Read input file:
fin = open(classinput, 'r')
lines = fin.readlines()

HasGal   = 0
HasKappa = 0
# LOOP over lines:
for line in lines:
    # Avoid comments:
    if line[0]!='#':
        # Find an input: 
        if '=' in line:
            eqpos = line.index('=')
            # Count number of fields:
            if 'output' == line[:eqpos] or 'output'==line.split()[0]:
                words = line[eqpos+1:].split(',')
                nf    = len(words)
                if 'nCl' in line[eqpos+1:]:
                    HasGal   = 1
                if 'sCl' in line[eqpos+1:]:
                    HasKappa = 1
                if HasGal+HasKappa!=nf:
                    print("ERROR: unkown field settings in output.")
                    sys.exit()
            # Count number of redshift bins and get their means:
            if 'selection_mean' == line[:eqpos] or 'selection_mean'==line.split()[0]:
                words = line[eqpos+1:].split(',')
                nz    = len(words)
                meanz = [float(z) for z in words]
            # Get the bins width:
            if 'selection_width' == line[:eqpos] or 'selection_width'==line.split()[0]:
                words      = line[eqpos+1:].split(',')
                halfwidthz = [float(dz) for dz in words]
                if len(halfwidthz) == 1:
                    halfwidithz = halfwidthz * nz;
                elif len(halfwidthz) != nz:
                    print("ERROR: redshift bins are not well defined.")
                    sys.exit()

fin = open(classinput, 'r')
lines = fin.readlines()

HasGal   = 0
HasKappa = 0
# LOOP over lines:
for line in lines:
    # Avoid comments:
    if line[0]!='#':
        # Find an input: 
        if '=' in line:
            eqpos = line.index('=')
            # Count number of fields:
            if 'output' == line[:eqpos] or 'output'==line.split()[0]:
                words = line[eqpos+1:].split(',')
                nf    = len(words)
                if 'nCl' in line[eqpos+1:]:
                    HasGal   = 1
                if 'sCl' in line[eqpos+1:]:
                    HasKappa = 1
                if HasGal+HasKappa!=nf:
                    print("ERROR: unkown field settings in output.")
                    sys.exit()
            # Count number of redshift bins and get their means:
            if 'selection_mean' == line[:eqpos] or 'selection_mean'==line.split()[0]:
                words = line[eqpos+1:].split(',')
                nz    = len(words)
                meanz = [float(z) for z in words]
            # Get the bins width:
            if 'selection_width' == line[:eqpos] or 'selection_width'==line.split()[0]:
                words      = line[eqpos+1:].split(',')
                halfwidthz = [float(dz) for dz in words]
                if len(halfwidthz) == 1:
                    halfwidthz = halfwidthz * nz;

# Convergence kappa shift formula from Hilbert, Hartlap & Schneider (2011)
def HilbertShift(z):
    return 0.008*z + 0.029*(z**2) - 0.0079*(z**3) + 0.00065*(z**4) 

def XavierShift(z):
    a0 = 0.2;
    s0 = 0.568591;
    return a0*(((z*s0)**2 + z*s0 + 1)/(z*s0 + 1) - 1)

# Functions for output:
def mean(f):
    m = [GalMean, KappaMean]
    if nf==2:
        return m[f-1]
    elif nf==1:
        if HasGal==1: 
            return GalMean
        if HasKappa==1:
            return KappaMean
# Functions for output:
def shift(f, z):
    s = [GalShift, KappaShift]
    if nf==2:
        if f==1:
            return GalShift
        if f==2:
            if FixKappa==1:
                return KappaShift
            if FixKappa==0:
                #return np.interp(z, fileZ, fileSh)
                #return HilbertShift(z)
                return XavierShift(z)
    elif nf==1:
        if HasGal==1: 
            return GalShift
        if HasKappa==1:
            if FixKappa==1:
                return KappaShift
            if FixKappa==0:
                #return np.interp(z, fileZ, fileSh)
                #return HilbertShift(z)
                return XavierShift(z)

# Functions for output:
def ftype(f):
    t = [GalType, KappaType]
    if nf==2:
        return t[f-1]
    elif nf==1:
        if HasGal==1: 
            return GalType
        if HasKappa==1:
            return KappaType


# Output:
fout = open(fieldinfo, 'w')

#print >>fout, "# Field number, z bin number, mean, shift, field type, zmin, zmax"
print("# Field number, z bin number, mean, shift, field type, zmin, zmax", end="\n", file=fout)
#print >>fout, "# Types: 1-galaxies 2-shear\n"
print("# Types: 1-galaxies 2-shear\n", end="", file=fout)

for f in range(1,nf+1):
    for z in range(1,nz+1):
        #print >>fout,'{0:6d} {1:6d}   {2:.4f}   {3:.4f} {4:6d}   {5:.4f}   {6:.4f}'.format(f, z, mean(f), shift(f, meanz[z-1]), ftype(f), meanz[z-1]-halfwidthz[z-1], meanz[z-1]+halfwidthz[z-1])
        print('{0:6d} {1:6d}   {2:.4f}   {3:.4f} {4:6d}   {5:.4f}   {6:.4f}'.format(f, z, mean(f), shift(f, meanz[z-1]), ftype(f), meanz[z-1]-halfwidthz[z-1], meanz[z-1]+halfwidthz[z-1]), end="\n", file=fout)