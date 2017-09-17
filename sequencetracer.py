#! /usr/bin/python3


# This work was inspired by Zooko O'Whielacronx's trace.py

# See Readme.md about usage and To-Dos

import sys
import linecache
import os, os.path

FILENAME = "output.sdiag"

# Make functions appear as separated objects
SEPARATE_FUNCTION_CALLS = True
LOGLEVEL = 1

class Diagram:
    def __init__(self):
        self.content=[]

    def append(self, line):
        self.content.append(line)

    def getcontent(self):
        return self.content

class SequenceTracer:
    def __init__(self, argv):

        self.stack = []
        self.diag = None
        self.list_of_functions=[]
        self.recorded_calls=0
        self.call_depth=0
        self.call_depth_max=0
        self.inputfilename = argv[1]
        self.argv=argv
        self.startpath=os.getcwd()
        self.endpath=None

    def localtracer(self, frame, event, arg):
        #print (event)
        #print (type(frame))
        line=frame.f_lineno
        filename = os.path.basename( frame.f_code.co_filename )
        code=linecache.getline(filename, line)
        if event == "return":
            self.call_depth -=1
            if len(self.stack)>=2:
                self.diag.append( "    "+ " "*self.call_depth + self.stack[-2][0]
                        + " <-- " + self.stack[-1][0] + ";\n")
            del self.stack[-1]
        if LOGLEVEL >2:
            print( "localtrace", event, filename, line, '::',  code)

    def globaltrace(self, frame, event, arg):
        #print(event)
        #print(type(frame))
        line=frame.f_lineno
        filename = os.path.basename( frame.f_code.co_filename )
        name = frame.f_code.co_name
        code=linecache.getline(filename, line)
        objectid="noid"
        # inspect analysis howto:
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
                    self.list_of_functions.append(classname)
                else:
                    self.list_of_functions.append(classname + '_' +name)

        if LOGLEVEL >2:
            print( "globaltrace", event, filename, line, classname,
                   objectid, name, '::', code)

        if event=="call":
            self.recorded_calls += 1
            if self.stack:
                line_begin= "    " + " "*self.call_depth + self.stack[-1][0] + " -> "
                self.call_depth += 1
                if self.call_depth > self.call_depth_max:
                    self.call_depth_max = self.call_depth
                if SEPARATE_FUNCTION_CALLS and not "self" in frame.f_locals:
                    if name == '<module>':
                        # E.g. Use None instead of "None_<module>"
                        self.stack.append((classname, name))
                    else:
                        self.stack.append((classname + '_' +name, name))
                else:
                    self.stack.append((classname, name))

                line_end = self.stack[-1][0] + " [label = \"" +self.stack[-1][1] + "\"];\n"
                self.diag.append(line_begin+line_end)
            else:
                self.stack.append((classname,name))

        if LOGLEVEL>3:
            print(self.stack)
        return self.localtracer

    def start(self):

        print('Starting SequenceTracer for %s'%self.inputfilename)

        # print( "file: %s" %__file__)
        # print( "name: %s" %__name__)
        # print( "package: %s" %__package__)


        #print(GLOBALS)

        self.diag=Diagram()

        # TODO: Add oportunity to do this as well
        # Simple exec
        # exec(cmd)

        # Exec that loads and execute a file without the need of an import
        code = compile(open(self.inputfilename).read(), self.inputfilename, 'exec')
        base = os.path.basename(self.inputfilename)

        # Create emulation of global symbol table for the script
        myglobals = {
            '__file__' : base,
            '__name__' : '__main__',
            '__package__' : None,
            '__cached__' : None,
        }

        #print (myglobals)

        # Make some backup copies
        argv_orig = self.argv[:]
        path_orig = sys.path[:]
        cwd_orig = os.getcwd()

        # Set sys.argv to the value our script will expect
        # argv0 will be the filename. However, when we call it from somewhere else
        # it will contain a path to the script.
        sys.argv=[]
        sys.argv.append(self.inputfilename) # has to be a relative path
        for arg in range(1, len(self.argv)-1):
            sys.argv.append(self.argv[arg+1])

        print('Prepared new argv', self.argv)

        # Set sys.path to the directory where inputile is. Same as when we call
        # it ourself
        sys.path[0] = os.path.dirname(self.inputfilename)

        print('## Execution of %s starts ##'%os.path.basename(self.inputfilename))
        # start tracing
        sys.settrace(self.globaltrace)
        exec(code, myglobals, myglobals)
        # disable tracing
        sys.settrace(None)
        print('## Execution of %s has ended ##'%os.path.basename(self.inputfilename))

        # Restore path values from backup
        self.argv = argv_orig
        sys.path = path_orig
        os.chdir(cwd_orig)

        self.endpath = os.getcwd()
        if self.startpath != self.endpath:
            print( "The path was changed by the called script.",
                self.startpath, self.endpath)

        print('Recorded %i method/function calls'%self.recorded_calls)
        print('Maximal call depth is %i'%self.call_depth_max)

        print('Writing diagram to %s'%FILENAME)
        myfile=open(FILENAME, 'w')
        myfile.write("seqdiag {\n")
        myfile.write("    edge_length = 140;\n")  # default value is 192
        myfile.write("    span_height = 5;\n")  # default value is 40

        if SEPARATE_FUNCTION_CALLS:
            myfile.write('    ')
            for function in self.list_of_functions:
                myfile.write(function+';')
            myfile.write('\n')

        for content in self.diag.getcontent():
            # the first filter
            if 'Class_EncodedFile' not in content:
                myfile.write(content)

        myfile.write("}\n")
        myfile.close()
        print('Exiting SequenceTracer')

if __name__ == '__main__':
    tracer=SequenceTracer(sys.argv)
    tracer.start()
