#! /usr/bin/python3


# This work was inspired by Zooko O'Whielacronx's trace.py

# See Readme.md about usage and To-Dos

import sys
import linecache
import os, os.path

stack = []
FILENAME = "output.sdiag"

# Make functions appear as separated objects
SEPARATE_FUNCTION_CALLS = False
LOGLEVEL = 1

list_of_functions = []
myfile = None
diag = None
recorded_calls=0

GLOBALS=globals()

class Diagram:
    def __init__(self):
        self.content=[]

    def append(self, line):
        self.content.append(line)

    def getcontent(self):
        return self.content

def localtracer(frame, event, arg):
    #print (event)
    #print (type(frame))
    line=frame.f_lineno
    filename = os.path.basename( frame.f_code.co_filename )
    code=linecache.getline(filename, line)
    if event == "return":
        if len(stack)>=2:
            diag.append( "    " + stack[-2][0] + " <-- " + stack[-1][0] + ";\n")
        del stack[-1]
    if LOGLEVEL >2:
        print( "localtrace", event, filename, line, '::',  code)

def globaltrace(frame, event, arg):
    #print(event)
    #print(type(frame))
    line=frame.f_lineno
    filename = os.path.basename( frame.f_code.co_filename )
    name = frame.f_code.co_name
    code=linecache.getline(filename, line)
    objectid="noid"
    # inspect analysis:
    # frame this is the frame
    # frame.f_locals these are the locals seen by the frame
    # frame.f_locals["self"] this is the reference to "self"
    # frame.f_locals["self"].__class__  this is the class it belongs to

    if "self" in frame.f_locals:
        # frame.f_locals["self"].__class__ # this is the object

        classname= 'Class_'+frame.f_locals["self"].__class__.__qualname__
        objectid='_id_' + hex(id( frame.f_locals["self"]))
        classname += objectid
    else:
        classname='None'
        if SEPARATE_FUNCTION_CALLS:
            if name == '<module>': # wtf
                list_of_functions.append(classname)
            else:
                list_of_functions.append(classname + '_' +name)

    if LOGLEVEL >2:
        print( "globaltrace", event, filename, line, classname, objectid, name, '::', code)

    if event=="call":
        global recorded_calls
        recorded_calls += 1
        if stack:
            diag.append( "    " + stack[-1][0] + " -> ")
            if SEPARATE_FUNCTION_CALLS and not "self" in frame.f_locals:
                if name == '<module>':
                    stack.append((classname, name)) # E.g. Use None instead of None_<module>
                else:
                    stack.append((classname + '_' +name, name))
            else:
                stack.append((classname, name))

            diag.append( stack[-1][0] + " [label = \"" +stack[-1][1] + "\"];\n")
        else:
            stack.append((classname,name))

    if LOGLEVEL>3:
        print(stack)
    return localtracer

def print_help():
    print("the wrong help")

def main(argv):

    inputfilename = argv[1]
    startpath=os.getcwd()
    print('Starting SequenceTracer for %s'%inputfilename)

    # print( "file: %s" %__file__)
    # print( "name: %s" %__name__)
    # print( "package: %s" %__package__)


    #print(GLOBALS)

    global diag
    diag=Diagram()

    # TODO: Add oportunity to do this as well
    # Simple exec
    # exec(cmd)

    # Exec that loads and execute a file without the need of an import
    code = compile(open(inputfilename).read(), inputfilename, 'exec')
    base = os.path.basename(inputfilename)

    # Create emulation of global symbol table for the script
    myglobals = {
        '__file__' : base,
        '__name__' : '__main__',
        '__package__' : None,
        '__cached__' : None,
    }

    #print (myglobals)

    # Make some backup copies
    argv_orig = argv[:]
    path_orig = sys.path[:]
    cwd_orig = os.getcwd()

    # Set sys.argv to the value our script will expect
    # argv0 will be the filename. However, when we call it from somewhere else
    # it will contain a path to the script.
    sys.argv[0]=inputfilename # has to be a relative path
    for arg in range(1, len(argv)-1):
        sys.argv[arg]= argv[arg+1]
    del sys.argv[-1]

    print('Prepared new argv', argv)

    # Set sys.path to the directory where inputile is. Same as when we call
    # it ourself
    sys.path[0] = os.path.dirname(inputfilename)

    print('## Execution of %s starts ##'%os.path.basename(inputfilename))
    # start tracing
    sys.settrace(globaltrace)
    exec(code, myglobals, myglobals)
    # disable tracing
    sys.settrace(None)
    print('## Execution of %s has ended ##'%os.path.basename(inputfilename))


    # Restore path values from backup
    argv = argv_orig
    sys.path = path_orig
    os.chdir(cwd_orig)

    endpath=os.getcwd()
    if startpath != endpath:
        print( "The path was changed by the called script.", startpath, endpath)

    global recorded_calls
    print('Recorded %i method/function calls'%recorded_calls)

    global myfile
    print('Writing diagram to %s'%FILENAME)
    myfile=open(FILENAME, 'w')
    myfile.write("seqdiag {\n")
    myfile.write("    edge_length = 140;\n")  # default value is 192
    myfile.write("    span_height = 5;\n")  # default value is 40

    if SEPARATE_FUNCTION_CALLS:
        myfile.write('    ')
        for function in list_of_functions:
            myfile.write(function+';')
        myfile.write('\n')

    for c in diag.getcontent():
        myfile.write(c)

    myfile.write("}\n")
    myfile.close()
    print('Exiting SequenceTracer')

if __name__ == '__main__':
    main(sys.argv)
