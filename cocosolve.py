#!/usr/bin/python

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

parser.add_argument('-q',
        dest='quiet',
        action="store_true",
        default=False,
        help="be extra quiet (no output)")

parser.add_argument('-m',
        dest='max_iter',
        action="store",
        default=0,
        type=int,
        help="max number of iterations")

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
        if args.max_iter and niter > args.max_iter:
            print("Max number of iterations reached ({0})\n".format(args.max_iter))
            cube.show()
            break
    
        # It fits?:
        if cube.fits():
            if cube.ipos > 4:
                # Then it's solved:
                if not args.quiet:
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
