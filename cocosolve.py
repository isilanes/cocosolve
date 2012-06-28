#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

# Initialize cube:
cube = C.Cube()

# Insert pieces:
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0])
cube.pieces.append([ 0 for x in range(12) ] + [1 for x in range(4)] )
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f'])

# Print out input:
print("Input pieces:\n")
cube.show()

remaining = True
while remaining:
    # It fits?:
    if cube.fits():
        if cube.ipos > 4:
            print("Solution:\n")
            cube.show()
            sys.exit()
        else:
            # Move on to next position:
            cube.ipos += 1
            print(cube.ipos)
            j = 1
            while cube.taken[j]:
                j += 1
            cube.faces[cube.ipos] = [j,0,0]
            cube.taken[j] = True
    else:
        # Try next combination:
        remaining = cube.next()
    
    # If we exhausted all combinations thus far, we need to backtrack:
    if not remaining:
        if cube.ipos > 1:
            print("backtrack")
            cube.show()
        else:
            # If we reach here it means we exhausted the loop and found no solution:
            print("No solution")
            sys.exit()
