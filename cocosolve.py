#!/usr/bin/python

import sys
import modules.core as C

#------------------------------------------------------------------------------#

# Initialize cube:
cube = C.Cube()

# Insert pieces:
cube.pieces.append([ [1,2,3,4,5], [6,7,8,9,0], ['a','b','c','d','e'], ['f','g','h','i','j'] ])
cube.pieces.append([ [0,0,0,0,1], [1,1,1,1,1], [1,1,1,1,1], [1,0,0,0,0] ])
cube.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
cube.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
cube.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
cube.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
#cube.pieces.append([ [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0] ])

C.manipulate(cube.pieces[0], 0, 1)
sys.exit()
cube.show()

# Solving loop:
solved = False
while not solved:
    fit = C.fit()
    while not fit:
        ok = C.next()
        if not ok:
            break
        fit = C.fit()

    if ok:
        # Follow with next face
        print("---\n")
        C.show()
        C.iface += 1

    else:
        # Backtrack
        C.iface -= 1
        C.next()
        print("backtrack")
        C.show()
        sys.exit()
        
    if C.iface > 5:
        solved = True

# Show result:
print("Success!!")
C.show()
