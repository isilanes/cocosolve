# -*- coding=utf-8 -*-

# Our libs:
from libcocosolve import core

# Functions:
def main():
    """Main loop."""

    # Get options from cli arguments:
    opts = core.parse_args()

    # Process input files:
    for infile in opts.infiles:
        # Initialize cube:
        cube = core.Cube()
        cube.read(infile)
        
        if opts.verbose:
            cube.show()
            
        # Total number of iterations:
        niter = 0
        
        remaining = True
        while remaining:
            if opts.verbose:
                cube.show_status()

            niter += 1
            if opts.max_iter and niter > opts.max_iter:
                print("Max number of iterations reached ({0})\n".format(opts.max_iter))
                cube.show()
                break
        
            # It fits?:
            if cube.fits():
                if cube.ipos > 4:
                    # Then it's solved:
                    if not opts.quiet:
                        print("Solution:\n")
                        cube.show()
                        cube.showdata(niter)
                    break
                else:
                    # Move on to next position:
                    cube.forward()
            else:
                # Try next combination:
                remaining = cube.next()
            
            # If we exhausted all combinations thus far, we need to backtrack:
            if not remaining:
                cube.backtrack()
                remaining = True


# Main loop:
if __name__ == "__main__":
    main()

