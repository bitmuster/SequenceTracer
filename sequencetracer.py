#! /usr/bin/python3


# This work was inspired by Zooko O'Whielacronx's trace.py


import sys
import linecache
import os, os.path

scipt_path = "/home/micha/Dump/CodeLand/AnyMate"
cmd = "AnyMate.main( ['AnyMate.py', '--nogui', 'greet', '../AnyMate/template.anymate'] ) "

scipt_path = "./"
cmd = "sample_code.main()"

sys.path.append(scipt_path)

#import AnyMate
import sample_code

stack=[]
FILENAME="output.sdiag"
myfile=None

def localtracer(frame, event, arg):
    #print (event)
    #print (type(frame))
    line=frame.f_lineno
    filename = os.path.basename( frame.f_code.co_filename )
    code=linecache.getline(filename, line)
    if event == "return":
        if len(stack)>=2:
            myfile.write( "    " + stack[-2][0] + " <-- " + stack[-1][0] + ";\n")
        del stack[-1]
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
        classname='Class_'+'none'
    print( "globaltrace", event, filename, line, classname, objectid, name, '::', code)
    if event=="call":
        if stack:
            myfile.write( "    " + stack[-1][0] + " -> ")
            stack.append((classname,name))
            myfile.write( stack[-1][0] + " [label = \"" +stack[-1][1] + "\"];\n")
        else:
            stack.append((classname,name))

    #print(stack)
    return localtracer



def main():
    global myfile
    myfile=open(FILENAME, 'w')
    sys.settrace(globaltrace)

    myfile.write("seqdiag {\n")

    exec(cmd)

    # disable tracing, otherwise we cannot close the file
    sys.settrace(None)
    myfile.write("}\n")
    myfile.close()

main()
