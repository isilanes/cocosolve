#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

# Initialize cube:
cube = C.Cube()

# Read pieces from file:
if len(sys.argv) > 1:
    cube.read(sys.argv[1])
else:
    sys.exit()

cube.show()
# Total number of iterations:
niter = 0

remaining = True
while remaining:
    print(cube.taken)
    print(cube.faces, end='')
    niter += 1
    #print(niter)
    if niter > 20:
        print("\n")
        cube.show()
        sys.exit()

    # It fits?:
    if cube.fits():
        print(" <-- fits {0}".format(cube.ipos))
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
        print()
        # Try next combination:
        remaining = cube.next()
    
    # If we exhausted all combinations thus far, we need to backtrack:
    if not remaining:
        print('^')
        cube.backtrack()
        remaining = True
