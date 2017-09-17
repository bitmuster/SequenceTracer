#! /usr/bin/python3


# This work was inspired by Zooko O'Whielacronx's trace.py

# See Readme.md about To-Dos

import sys
import linecache
import os, os.path

stack=[]
FILENAME="output.sdiag"

# Make functions appear as separated objects
SEPARATE_FUNCTION_CALLS=False
LOGLEVEL=1

list_of_functions=[]
myfile=None
diag=None

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

    #print(stack)
    return localtracer

def abspath_impl(s):
    print('Puke')

def print_help():
    print("the wrong help")

def main():

    inputfilename = sys.argv[1]
    startpath=os.getcwd()
    print('Starting SequenceTracer for %s'%inputfilename)

    print( "file: %s" %__file__)
    print( "name: %s" %__name__)
    print( "package: %s" %__package__)
    #print( "cached: %s" %__cached__) # Exists only when we debug it WTF
    #print( "path: %s" %__path__)

    print('* argv[0]                  :' + sys.argv[0])
    print('* os.path.abspath(argv[0]) :' + os.path.abspath(sys.argv[0]))
    print('* os.path.dirname(argv[0]) :' + os.path.dirname(sys.argv[0]))
    print('* os.path.abspath(os.path.dirname(sys.argv[0])) :' + os.path.abspath(os.path.dirname(sys.argv[0])))

    print(GLOBALS)

    global diag
    diag=Diagram()
    sys.settrace(globaltrace)

    # Simple exec:
    # exec(cmd)

    # Exec that loads and execute a file without the need of an import
    # TODO: How to deal with command line parameters? Can we inject argv?
    code = compile(open(inputfilename).read(), inputfilename, 'exec')
    base = os.path.basename(inputfilename)

    # Create emulation of global symbol table for the script
    # even now, argv and sys.path are taken from this script WTF
    myglobals = {
        '__file__' : base,
        '__name__' : '__main__',
        '__package__' : None,
        '__cached__' : None,
        'sys' : sys
    }

    print (myglobals)

    # Set argv to the value our script will expect
    sys.argv[0]=os.path.basename(inputfilename)
    #del sys.argv[1]
    del sys.argv[2]
    sys.argv[1]='template.anymate'
    sys.path[0] = os.path.dirname(inputfilename)

    myglobals['sys'].abspath=abspath_impl

    print('## Execution of %s starts ##'%os.path.basename(inputfilename))
    exec(code, myglobals, myglobals)
    print('## Execution of %s has ended ##'%os.path.basename(inputfilename))

    # disable tracing, otherwise we cannot close the file
    sys.settrace(None)

    endpath=os.getcwd()
    if startpath != endpath:
        print( "The path was changed by the called script.", startpath, endpath)


    global myfile
    print('Writing diagram to %s'%FILENAME)
    myfile=open(FILENAME, 'w')
    myfile.write("seqdiag {\n")
    myfile.write("    edge_length = 140;\n")  # default value is 192
    myfile.write("    span_height = 5;\n")  # default value is 40

    if SEPARATE_FUNCTION_CALLS:
        for function in list_of_functions:
            myfile.write(function+';')
        myfile.write('\n')

    for c in diag.getcontent():
        myfile.write(c)

    myfile.write("}\n")
    myfile.close()
    print('Exiting SequenceTracer')

main()
