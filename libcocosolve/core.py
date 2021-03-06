"""Core module for cocosolve."""

# Standard libs:
import os
import sys
import argparse

# Functions:
def parse_args(arguments=sys.argv[1:]):
    """Parse command-line arguments, and return parsed options."""

    parser = argparse.ArgumentParser()

    parser.add_argument('infiles',
            metavar="infile",
            nargs="+",
            help="one or more input file(s)")

    parser.add_argument('-v', "--verbose",
            help="Be verbose. Default: do not be.",
            action="store_true",
            default=False)

    parser.add_argument('-q', "--quiet",
            help="Be extra quiet (no output). Default: do not be.",
            action="store_true",
            default=False)

    parser.add_argument('-m', '--max_iter',
            help="Max number of iterations. Default: 0 (no limit).",
            type=int,
            default=0)


    return parser.parse_args(arguments)

def compat(sa, sb):
    """Return True if sides sa and sb are compatible. False, otherwise."""

    for i in range(3):
        try:
            if not sa[i] + sb[2-i] == 1:
                return False
        except:
            return False

    return True

def manipulate(piece, flip, rot):
    """Returns piece (array of 16 0/1 elements), representing input piece 
    flipped (flip = 1) or not (flip = 0), and rotated rot times CCW.
    """
    # Copy original piece:
    m = piece[:]

    # Flip?
    if flip:
        m.reverse()
        m = m[-5:] + m[:11]

    # Rotate?:
    cut = (rot % 4) * 4
    m = m[cut:] + m[:cut]

    return m


# Classes:
class Cube(object):
    """All info and methods for a give cube."""
    
    # Constructor:
    def __init__(self):
        self.pieces = []
        # self.faces: ith element contains [j,k,l] triplet, meaning jth piece
        # is placed in ith face, with orientation l (l = 0, upwards, then 
        # 1,2,3 -> 90º rotation CCW), and facing k (k = 0, outward; k = 1, inward)
        self.faces = [ [0,0,0], [1,0,0], [2,0,0], [3,0,0], [4,0,0], [5,0,0] ]
        self.ipos = 1
        self.taken = [ True, False, False, False, False, False ]


    # Public methods:
    def next(self):
        n, flip, rot = self.faces[self.ipos]

        if rot < 3:
            rot += 1
        elif not flip:
            flip = 1
            rot = 0
        elif n < 5:
            self.taken[n] = False # release current piece, to jump to next
            flip = 0
            rot = 0
            n += 1
            while self.taken[n] and n < 5:
                n += 1
        else:
            if self.ipos == 1:
                # Mmm, first piece and no possible match? Backtrack won't
                # fix this: there is no solution.
                print("No solution!")
                sys.exit()
            else:
                # We need to backtrack:
                return False

        self.faces[self.ipos] = [n, flip, rot]
        return True

    def fits(self):
        n, flip, rot = self.faces[self.ipos]
        self.taken[n] = True
        current = manipulate(self.pieces[n], flip, rot)

        if self.ipos == 1:
            # Make North of piece 1 match South of piece 0:
            sn1 = current[1:4]
            ss0 = self.pieces[0][9:12]
            if not compat(sn1, ss0):
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

        # If we reach so far, it means it fits:
        return True

    def show(self):
        tile = ['·', 'o']

        # Face 0:
        string  = '           '
        for v in self.pieces[0][:5]:
            string += '{0} '.format(tile[v])
        string += '         \n'
        for i in range(3):
            tag = ' '
            if i == 1:
                tag = '0'
            string += '           '
            string += '{0}   {2}   {1}'.format(tile[self.pieces[0][15-i]], tile[self.pieces[0][5+i]], tag)
            string += '         \n'
        string  += '           '
        for i in range(5):
            string += '{0} '.format(tile[self.pieces[0][12-i]])
        string += '         \n\n'

        # Faces 3, 1, 2:
        n, flip, rot = self.faces[3]
        piece3 = manipulate(self.pieces[n], flip, rot)
        n, flip, rot = self.faces[1]
        piece1 = manipulate(self.pieces[n], flip, rot)
        n, flip, rot = self.faces[2]
        piece2 = manipulate(self.pieces[n], flip, rot)

        for v in piece3[:5]:
            string += '{0} '.format(tile[v])
        string += ' '

        for v in piece1[:5]:
            string += '{0} '.format(tile[v])
        string += ' '

        for v in piece2[:5]:
            string += '{0} '.format(tile[v])
        string += '\n'

        for i in range(3):
            tag3, tag1, tag2 = ' ', ' ', ' '
            if i == 1:
                tag3 = '{0}'.format(self.faces[3][0])
                tag1 = '{0}'.format(self.faces[1][0])
                tag2 = '{0}'.format(self.faces[2][0])
            string += '{0}   {2}   {1}  '.format(tile[piece3[15-i]], tile[piece3[5+i]], tag3)
            string += '{0}   {2}   {1}  '.format(tile[piece1[15-i]], tile[piece1[5+i]], tag1)
            string += '{0}   {2}   {1}  '.format(tile[piece2[15-i]], tile[piece2[5+i]], tag2)
            string += '\n'

        for i in range(5):
            string += '{0} '.format(tile[piece3[12-i]])
        string += ' '

        for i in range(5):
            string += '{0} '.format(tile[piece1[12-i]])
        string += ' '

        for i in range(5):
            string += '{0} '.format(tile[piece2[12-i]])
        string += '\n\n'

        # Faces 4 and 5:
        for j in [4,5]:
            n, flip, rot = self.faces[j]
            piece = manipulate(self.pieces[n], flip, rot)
            string  += '           '
            for v in piece[:5]:
                string += '{0} '.format(tile[v])
            string += '\n'
            for i in range(3):
                tag = ' '
                if i == 1:
                    tag = '{0}'.format(self.faces[j][0])
                string += '           {0}   {2}   {1}'.format(tile[piece[15-i]], tile[piece[5+i]], tag)
                string += '\n'
            
            string += '           '
            for i in range(5):
                string += '{0} '.format(tile[piece[12-i]])
            string += '\n\n'
        
        print(string)

    def showdata(self, niter=0):
        """Show different facts about the run."""
        
        print("Iterations = {0}".format(niter))
        print("Face arrangement:")
        for face in self.faces:
            string = 'Piece {0[0]} -> flip {0[1]}, rot {0[2]}'.format(face)
            print(string)

    def read(self, fn=None):
        """Read input info from file named "fn"."""

        if not fn or not os.path.isfile(fn):
            print("No valid input file given!")
            sys.exit()

        with open(fn, 'r') as f:
            for line in f:
                list = [ int(x) for x in line.strip() ]
                self.pieces.append(list)

    def forward(self):
        """Move on to next position."""

        self.ipos += 1

        # Propose for next position the first non-already-taken piece:
        first = 0
        for taken in self.taken:
            if not taken:
                self.faces[self.ipos] = [first, 0, 0]
                break
            else:
                first += 1

    def backtrack(self):
        """Backtrack one position."""

        # If asked to backtrack when already at first position, it means
        # there is no solution:
        if self.ipos == 1:
            print("No solution!")
            sys.exit()

        # Else, go back:
        self.ipos -= 1
        rem = self.next() # "add 1" to previous state, to not repeat it

        # Backtrack again if last "next" went over the top:
        if not rem:
            self.backtrack()

    def show_status(self):
        strings = []
        for i in range(self.ipos+1):
            string = '{0[0]}{0[1]}{0[2]}'.format(self.faces[i])
            strings.append(string)

        print('-'.join(strings))

