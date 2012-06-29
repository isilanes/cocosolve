'''Core module for cocosolve.'''

#------------------------------------------------------------------------------#

def compat(sa, sb):
    for i in range(3):
        try:
            if not sa[i] + sb[2-i] == 1:
                return False
        except:
            return False

    return True

#------------------------------------------------------------------------------#

def manipulate(piece, flip, rot):
    '''Returns piece (array of 16 0/1 elements), representing input piece 
    flipped (flip = 1) or not (flip = 0), and rotated rot times CCW.'''

    # Copy original piece:
    m = piece[:]

    # Flip?
    if flip:
        m.reverse()
        m = m[-5:] + m[:11]

    # Rotate?:
    for i in range(rot):
        m = m[4:] + m[:4]

    return m

#------------------------------------------------------------------------------#

class Cube:
    
    def __init__(self):
        self.pieces = []
        # self.faces: ith element contains [j,k,l] triplet, meaning jth piece
        # is placed in ith face, with orientation l (l = 0, upwards, then 
        # 1,2,3 -> 90º rotation CCW), and facing k (k = 0, outward; k = 1, inward)
        self.faces = [ [0,0,0], [1,0,0], [2,0,0], [3,0,0], [4,0,0], [5,0,0] ]
        self.ipos = 1
        self.taken = { 0 : True, 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }

    # --- #

    def next(self):
        n, flip, rot = self.faces[self.ipos]

        if rot < 3:
            rot += 1
        elif not flip:
            flip = 1
            rot = 0
        elif n < 5:
            self.taken[n] = False # release current piece, to jump to next
            taken = True
            while n < 5 and taken:
                n += 1
                taken = self.taken[n]
                if not taken:
                    self.taken[n] = True
                    rot = 0
                    flip = 0
        else:
            return False

        self.faces[self.ipos] = [n, flip, rot]
        return True

    # --- #

    def fits(self):
        n, flip, rot = self.faces[self.ipos]
        self.taken[n] = False # release it, in case we exit because it doesn't fit
        current = manipulate(self.pieces[n], flip, rot)
        if self.ipos == 1:
            # Make North of piece 1 match South of piece 0:
            sn1 = current[1:4]
            ss0 = self.pieces[0][9:12]
            if not compat(sn1,ss0):
                return False

        elif self.ipos == 2:
            # Make W2 match E1:
            sw2 = current[13:]
            c2 = current[0]
            nb, flipb, rotb = self.faces[1]
            p1 = manipulate(self.pieces[nb], flipb, rotb)
            se1 = p1[5:8]
            c1 = p1[4]
            if not compat(sw2, se1):
                return False
            
            # Make N2 match E0:
            sn2 = current[1:4]
            se0 = self.pieces[0][5:8]
            c0 = self.pieces[0][8]
            if not compat(sn2, se0):
                return False

            # Make 2-1-0 corner fit:
            if not c2 + c1 + c0 == 1:
                return False

        elif self.ipos == 3:
            # Make E3 match W1:
            se3 = current[5:8]
            c3 = current[4]
            nb, flipb, rotb = self.faces[1]
            p1 = manipulate(self.pieces[nb], flipb, rotb)
            sw1 = p1[13:]
            c1 = p1[0]
            if not compat(se3, sw1):
                return False

            # Make N3 match E0:
            sn3 = current[1:4]
            se0 = self.pieces[0][13:]
            c0 = self.pieces[0][12]
            if not compat(sn3, se0):
                return False

            # Make 3-1-0 corner fit:
            if not c3 + c1 + c0 == 1:
                return False

        elif self.ipos == 4:
            # Make N4 match S1:
            sn4 = current[1:4]
            c4nw = current[0]
            c4ne = current[4]
            nb, flipb, rotb = self.faces[1]
            p1 = manipulate(self.pieces[nb], flipb, rotb)
            ss1 = p1[9:12]
            c1sw = p1[12]
            c1se = p1[8]
            if not compat(sn4, ss1):
                return False

            # Make E4 match S2:
            se4 = current[5:8]
            nb, flipb, rotb = self.faces[2]
            p2 = manipulate(self.pieces[nb], flipb, rotb)
            ss2 = p2[9:12]
            c2sw = p2[12]
            if not compat(se4, ss2):
                return False

            # Make W4 match S3:
            sw4 = current[13:]
            nb, flipb, rotb = self.faces[3]
            p3 = manipulate(self.pieces[nb], flipb, rotb)
            ss3 = p3[9:12]
            c3se = p3[8]
            if not compat(sw4, ss3):
                return False

            # Make 4-1-2 corner fit:
            if not c4ne + c1se + c2sw == 1:
                return False

            # Make 4-1-3 corner fit:
            if not c4nw + c1sw + c3se == 1:
                return False
            
        elif self.ipos == 5:
            # Make N5 and S4 match:
            sn5 = current[1:4]
            c5nw = current[0]
            c5ne = current[4]
            c5se = current[8]
            c5sw = current[12]
            nb, flipb, rotb = self.faces[4]
            p4 = manipulate(self.pieces[nb], flipb, rotb)
            ss4 = p4[9:12]
            c4sw = p4[12]
            c4se = p4[8]
            if not compat(sn5, ss4):
                return False

            # Make E5 and E2 match:
            se5 = current[5:8]
            nb, flipb, rotb = self.faces[2]
            p2 = manipulate(self.pieces[nb], flipb, rotb)
            se2 = p2[5:8]
            c2se = p2[8]
            c2ne = p2[4]
            if not compat(se5, se2):
                return False

            # Make W5 and W3 match:
            sw5 = current[13:]
            nb, flipb, rotb = self.faces[3]
            p3 = manipulate(self.pieces[nb], flipb, rotb)
            sw3 = p3[13:]
            c3nw = p3[0]
            c3sw = p3[12]
            if not compat(sw5, sw3):
                return False

            # Make S5 and N0 match:
            ss5 = current[9:12]
            sn0 = self.pieces[0][1:4]
            c0nw = self.pieces[0][0]
            c0ne = self.pieces[0][4]
            if not compat(ss5, sn0):
                return False

            # Make 5-4-2 corner fit:
            if not c5ne + c4se + c2se == 1:
                return False

            # Make 5-4-3 corner fit:
            if not c5nw + c4sw + c3sw == 1:
                return False

            # Make 5-2-0 corner fit:
            if not c5se + c2ne + c0ne == 1:
                return False

            # Make 5-3-0 corner fit:
            if not c5sw + c3nw + c0nw == 1:
                return False

        # If we reach so far, it means it fits. Say so, after reflagging
        # the piece as used.
        self.taken[n] = True
        return True
    # --- #

    def show(self):
        # Face 0:
        string  = '           '
        for v in self.pieces[0][:5]:
            string += '{0} '.format(v)
        string += '         \n'
        for i in range(3):
            tag = ' '
            if i == 1:
                tag = '0'
            string += '           '
            string += '{0}   {2}   {1}'.format(self.pieces[0][15-i], self.pieces[0][5+i], tag)
            string += '         \n'
        string  += '           '
        for i in range(5):
            string += '{0} '.format(self.pieces[0][12-i])
        string += '         \n\n'

        # Faces 3, 1, 2:
        n, flip, rot = self.faces[3]
        piece3 = manipulate(self.pieces[n], flip, rot)
        n, flip, rot = self.faces[1]
        piece1 = manipulate(self.pieces[n], flip, rot)
        n, flip, rot = self.faces[2]
        piece2 = manipulate(self.pieces[n], flip, rot)

        for v in piece3[:5]:
            string += '{0} '.format(v)
        string += ' '

        for v in piece1[:5]:
            string += '{0} '.format(v)
        string += ' '

        for v in piece2[:5]:
            string += '{0} '.format(v)
        string += '\n'

        for i in range(3):
            tag3, tag1, tag2 = ' ', ' ', ' '
            if i == 1:
                tag3 = '{0}'.format(self.faces[3][0])
                tag1 = '{0}'.format(self.faces[1][0])
                tag2 = '{0}'.format(self.faces[2][0])
            string += '{0}   {2}   {1}  '.format(piece3[15-i], piece3[5+i], tag3)
            string += '{0}   {2}   {1}  '.format(piece1[15-i], piece1[5+i], tag1)
            string += '{0}   {2}   {1}  '.format(piece2[15-i], piece2[5+i], tag2)
            string += '\n'

        for i in range(5):
            string += '{0} '.format(piece3[12-i])
        string += ' '

        for i in range(5):
            string += '{0} '.format(piece1[12-i])
        string += ' '

        for i in range(5):
            string += '{0} '.format(piece2[12-i])
        string += '\n\n'

        # Faces 4 and 5:
        for j in [4,5]:
            n, flip, rot = self.faces[j]
            piece = manipulate(self.pieces[n], flip, rot)
            string  += '           '
            for v in piece[:5]:
                string += '{0} '.format(v)
            string += '\n'
            for i in range(3):
                tag = ' '
                if i == 1:
                    tag = '{0}'.format(self.faces[j][0])
                string += '           {0}   {2}   {1}'.format(piece[15-i], piece[5+i], tag)
                string += '\n'
            
            string += '           '
            for i in range(5):
                string += '{0} '.format(piece[12-i])
            string += '\n\n'
        
        print(string)

#------------------------------------------------------------------------------#
