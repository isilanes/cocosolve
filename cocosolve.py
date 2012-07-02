#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

# Initialize cube:
cube = C.Cube()

# Insert pieces:

'''
# Ejemplo:
cube.pieces.append([0 for x in range(16) ])
cube.pieces.append([0,1,1,1,1,0,0,0,1,0,0,0,1,1,1,1])
cube.pieces.append([1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0])
cube.pieces.append([0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0])
cube.pieces.append([0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1])
cube.pieces.append([1,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1])
'''

# Azul:
cube.pieces.append([0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1])
cube.pieces.append([1,0,1,0,1,1,0,1,1,0,1,0,1,1,0,1])
cube.pieces.append([0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0])
cube.pieces.append([0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1])
cube.pieces.append([0,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1])
cube.pieces.append([0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0])

# Print out input:
#print("Input pieces:\n")
#cube.show()

# Total number of iterations:
niter = 0

remaining = True
while remaining:
    niter += 1
    # It fits?:
    if cube.fits():
        if cube.ipos > 4:
            print("Solution:\n")
            cube.show()
            cube.showdata(niter)
            sys.exit()
        else:
            # Move on to next position:
            cube.ipos += 1
            j = 1
            while cube.taken[j]:
                j += 1
                if j > 5:
                    print("No solution!")
                    sys.exit()
            cube.faces[cube.ipos] = [j,0,0]
            cube.taken[j] = True
    else:
        # Try next combination:
        remaining = cube.next()
    
    # If we exhausted all combinations thus far, we need to backtrack:
    if not remaining:
        if cube.ipos > 1:
            cube.ipos -= 1
            cube.next()
            remaining = True
        else:
            # If we reach here it means we exhausted the loop and found no solution:
            print("No solution")
            sys.exit()
