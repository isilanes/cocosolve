#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

verbose = False

# Initialize cube:
cube = C.Cube()

# Read pieces from file:
if len(sys.argv) > 1:
    cube.read(sys.argv[1])
else:
    sys.exit()

# Total number of iterations:
niter = 0

remaining = True
while remaining:
    if verbose:
        cube.show_status()
    niter += 1
    if niter > 10000:
        print("\n")
        cube.show()
        sys.exit()

    # It fits?:
    if cube.fits():
        if cube.ipos > 4:
            # Then it's solved:
            print("Solution:\n")
            cube.show()
            cube.showdata(niter)
            sys.exit()
        else:
            # Move on to next position:
            cube.forward()
    else:
        # Try next combination:
        remaining = cube.next()
    
    # If we exhausted all combinations thus far, we need to backtrack:
    if not remaining:
        if verbose:
            print('^')
        cube.backtrack()
        remaining = True
