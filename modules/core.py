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
            sa = current[1:4]
            sb = self.pieces[0][9:12]
            if not compat(sa,sb):
                return False

        elif self.ipos == 2:
            sa = current[12:] + current[:1]
            nb, flipb, rotb = self.faces[1]
            b = manipulate(self.pieces[nb], flipb, rotb)
            sb = b[4:9]
            print(n, sa, nb, sb)
            if not compat(sa,sb):
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
