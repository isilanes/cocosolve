#!/usr/bin/python

import sys
import argparse

from modules import core

#------------------------------------------------------------------------------#

parser = argparse.ArgumentParser()

parser.add_argument('infiles',
        metavar="infile",
        nargs="+",
        help="one or more input file(s)")

parser.add_argument('-v',
        dest='verbose',
        action="store_true",
        default=False,
        help="be verbose")

args = parser.parse_args()

#------------------------------------------------------------------------------#

for infile in args.infiles:
    # Initialize cube:
    cube = core.Cube()
    cube.read(infile)
    
    if args.verbose:
        cube.show()
        
    # Total number of iterations:
    niter = 0
    
    remaining = True
    while remaining:
        if args.verbose:
            cube.show_status()

        niter += 1
        if niter > 50000:
            print("Max reached\n")
            cube.show()
            sys.exit()
    
        # It fits?:
        if cube.fits():
            if cube.ipos > 4:
                # Then it's solved:
                print("Solution:\n")
                cube.show()
                cube.showdata(niter)
                break
            else:
                # Move on to next position:
                cube.forward()
        else:
            # Try next combination:
            remaining = cube.next()
        
        # If we exhausted all combinations thus far, we need to backtrack:
        if not remaining:
            cube.backtrack()
            remaining = True
