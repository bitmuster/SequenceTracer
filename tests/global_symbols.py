

import sys
import os

def main():

    print('Starting test global_symbols (', sys.argv[0], ') from folder ', sys.path[0])

    print(sys.argv)

    abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Everything we do now happens in this directory
    print('* argv[0]                  :' + sys.argv[0])
    print('* os.path.abspath(argv[0]) :' + os.path.abspath(sys.argv[0]))
    print('* os.path.dirname(argv[0]) :' + os.path.dirname(sys.argv[0]))
    print('* os.path.abspath(os.path.dirname(sys.argv[0])) :' + os.path.abspath(os.path.dirname(sys.argv[0])))
    os.chdir(abspath)

if __name__ == '__main__':

    print( "file: %s" %__file__)
    print( "name: %s" %__name__)
    print( "package: %s" %__package__)
    print( "cached: %s" %__cached__)

    main()