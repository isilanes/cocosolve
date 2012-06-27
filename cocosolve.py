#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

# Initialize cube:
cube = C.Cube()

# Insert pieces:
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f'])
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0 for x in range(16) ])
cube.pieces.append([ 0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f'])

# Print out input:
print("Input pieces:\n")
cube.show()

# If we exhaust this loop, we depleted all combinations (no solution):
remaining = True
while remaining:
    # Try next combination:
    remaining = cube.next()

    # It fits?:
    if cube.fits():
        cube.ipos += 1

# Print out output:
print("Output pieces:\n")
cube.show()

print("No solution")
sys.exit()
