#!/usr/bin/python

import sys

#------------------------------------------------------------------------------#

def compat(sa, sb):
    for i in range(5):
        if not sa[i] + sb[4-i] == 1:
            return False

    return True

#------------------------------------------------------------------------------#

class Cubo:
    
    def __init__(self):
        self.pieces = []
        # self.faces: ith element contains [j,k,l] triplet, meaning jth piece
        # is placed in ith face, with orientation k (k = 0, upwards, then 
        # 1,2,3 -> 90º rotation CCW), and facing l (l = 0, outward; l = 1, inward)
        self.faces = [ [0,0,0], [1,0,0], [2,0,0], [3,0,0], [4,0,0], [5,0,0] ]
        self.iface = 1
        self.taken = { 0 : True, 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }

    # --- #

    def next(self):
        p, d = self.faces[self.iface]
        if d < 3:
            d += 1
        elif p < 5:
            p += 1
            d = 0
        else:
            return False

        self.faces[self.iface] = [p, d]
        return True

    # --- #

    def fit(self):
        p, d = self.faces[self.iface]
        if self.iface == 1:
            sa = self.pieces[0][2]
            i, j = self.faces[1]
            sb = self.pieces[1][j]
            if not compat(sa, sb):
                return False

        elif self.iface == 2:
            pa, da = self.faces[2]
            pb, db = self.faces[1]
            
            fa = da + 3
            if fa > 3:
                fa += -4
            sa = self.pieces[pa][fa]

            fb = db + 1
            if fb > 3:
                fb += -4
            sb = self.pieces[pb][fb]

            if not compat(sa, sb):
                return False

        return True

    # --- #

    def place(self, iface, ipieza, idir):
        self.faces[iface] = [ipieza, idir]

    # --- #

    def show(self):
        # Face 0:
        string  = '           '
        for v in self.pieces[0][0]:
            string += '{0} '.format(v)
        string += '         \n'
        for i in range(1,4):
            tag = ' '
            if i == 2:
                tag = '0'
            string += '           '
            string += '{0}   {2}   {1}'.format(self.pieces[0][3][4-i], self.pieces[0][1][i], tag)
            string += '         \n'
        string  += '           '
        for i in range(5):
            string += '{0} '.format(self.pieces[0][2][4-i])
        string += '         \n\n'

        # Faces 3, 1, 2:
        p, d = self.faces[3]
        for v in self.pieces[p][d]:
            string += '{0} '.format(v)
        string += ' '

        p, d = self.faces[1]
        for v in self.pieces[p][d]:
            string += '{0} '.format(v)
        string += ' '

        p, d = self.faces[2]
        for v in self.pieces[p][d]:
            string += '{0} '.format(v)
        string += '\n'

        for i in range(1,4):
            p, d = self.faces[3]
            f1 = d + 1
            if f1 > 3:
                f1 += -4
            f2 = f1 + 2
            if f2 > 3:
                f2 += -4
            tag = ' '
            if i == 2:
                tag = '{0}'.format(self.faces[3][0])
            string += '{0}   {2}   {1}'.format(self.pieces[p][f2][4-i], self.pieces[p][f1][i], tag)

            string += '  '

            p, d = self.faces[1]
            f1 = d + 1
            if f1 > 3:
                f1 += -4
            f2 = f1 + 2
            if f2 > 3:
                f2 += -4
            if i == 2:
                tag = '{0}'.format(self.faces[1][0])
            string += '{0}   {2}   {1}'.format(self.pieces[p][f2][4-i], self.pieces[p][f1][i], tag)

            string += '  '

            p, d = self.faces[2]
            f1 = d + 1
            if f1 > 3:
                f1 += -4
            f2 = f1 + 2
            if f2 > 3:
                f2 += -4
            if i == 2:
                tag = '{0}'.format(self.faces[2][0])
            string += '{0}   {2}   {1}'.format(self.pieces[p][f2][4-i], self.pieces[p][f1][i], tag)

            string += '\n'

        p, d = self.faces[3]
        f = d + 2
        if f > 3:
             f += -4
        for i in range(5):
            string += '{0} '.format(self.pieces[p][f][4-i])

        string += ' '

        p, d = self.faces[1]
        f = d + 2
        if f > 3:
             f += -4
        for i in range(5):
            string += '{0} '.format(self.pieces[p][f][4-i])

        string += ' '

        p, d = self.faces[2]
        f = d + 2
        if f > 3:
             f += -4
        for i in range(5):
            string += '{0} '.format(self.pieces[p][f][4-i])

        string += '\n\n'

        # Faces 4 and 5:
        for j in [4,5]:
            string  += '           '
            p, d = self.faces[j]
            for v in self.pieces[p][d]:
                string += '{0} '.format(v)
            string += '         \n'
            for i in range(1,4):
                f1 = d + 1
                if f1 > 3:
                    f1 += -4
                f2 = f1 + 2
                if f2 > 3:
                    f2 += -4
                string += '           '
                tag = ' '
                if i == 2:
                    tag = '{0}'.format(self.faces[j][0])
                string += '{0}   {2}   {1}'.format(self.pieces[p][f2][4-i], self.pieces[p][f1][i], tag)
                string += '         \n'
            string  += '           '
            
            f = d + 2
            if f > 3:
                f += -4
            for i in range(5):
                string += '{0} '.format(self.pieces[p][f][4-i])
            string += '         \n\n'
        
        print(string)

#------------------------------------------------------------------------------#

# Initialize cube:
C = Cubo()

# Insert pieces:
C.pieces.append([ [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0] ])
C.pieces.append([ [0,0,0,0,1], [1,1,1,1,1], [1,1,1,1,1], [1,0,0,0,0] ])
C.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
C.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
C.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
C.pieces.append([ [1,1,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1] ])
#C.pieces.append([ [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0] ])

C.show()

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
