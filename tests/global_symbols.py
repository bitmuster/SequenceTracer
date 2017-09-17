
import sys
import os

expected_diagram="""seqdiag {
    edge_length = 140;
    span_height = 5;
    None -> None_print_stuff [label = "print_stuff"];
     None_print_stuff -> None_dirname [label = "dirname"];
      None_dirname -> None__get_sep [label = "_get_sep"];
      None_dirname <-- None__get_sep;
     None_print_stuff <-- None_dirname;
     None_print_stuff -> None_abspath [label = "abspath"];
      None_abspath -> None_isabs [label = "isabs"];
       None_isabs -> None__get_sep [label = "_get_sep"];
       None_isabs <-- None__get_sep;
      None_abspath <-- None_isabs;
      None_abspath -> None_join [label = "join"];
       None_join -> None__get_sep [label = "_get_sep"];
       None_join <-- None__get_sep;
      None_abspath <-- None_join;
      None_abspath -> None_normpath [label = "normpath"];
      None_abspath <-- None_normpath;
     None_print_stuff <-- None_abspath;
     None_print_stuff -> None_abspath [label = "abspath"];
      None_abspath -> None_isabs [label = "isabs"];
       None_isabs -> None__get_sep [label = "_get_sep"];
       None_isabs <-- None__get_sep;
      None_abspath <-- None_isabs;
      None_abspath -> None_join [label = "join"];
       None_join -> None__get_sep [label = "_get_sep"];
       None_join <-- None__get_sep;
      None_abspath <-- None_join;
      None_abspath -> None_normpath [label = "normpath"];
      None_abspath <-- None_normpath;
     None_print_stuff <-- None_abspath;
     None_print_stuff -> None_dirname [label = "dirname"];
      None_dirname -> None__get_sep [label = "_get_sep"];
      None_dirname <-- None__get_sep;
     None_print_stuff <-- None_dirname;
    None <-- None_print_stuff;
}
"""

def print_stuff():

    print('Starting test global_symbols (', sys.argv[0], ') from folder ', sys.path[0])

    print(sys.argv)

    abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Everything we do now happens in this directory
    print('* argv[0]                  :' + sys.argv[0])
    print('* os.path.abspath(argv[0]) :' + os.path.abspath(sys.argv[0]))
    print('* os.path.dirname(argv[0]) :' + os.path.dirname(sys.argv[0]))

if __name__ == '__main__':

    print( "file: %s" %__file__)
    print( "name: %s" %__name__)
    print( "package: %s" %__package__)
    print( "cached: %s" %__cached__)

    print_stuff()
