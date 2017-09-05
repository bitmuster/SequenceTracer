#! /usr/bin/python3

# 
# This work was inspired by Zooko O'Whielacronx's trace.py
#
# python3 sequencetracer.py  > diag.diag
# seqdiag3 -T svg diag.diag
#
import sys
import linecache

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
    filename=frame.f_code.co_filename
    code=linecache.getline(filename, line)
    if event == "return":
        if len(stack)>=2:
            myfile.write( "    " + stack[-2][0] + " <-- " + stack[-1][0] + ";\n")
        del stack[-1]
    #print( "local ", event, filename, line, code)

def globaltrace(frame, event, arg):
    #print(event)
    #print(type(frame))
    line=frame.f_lineno
    filename=frame.f_code.co_filename
    name = frame.f_code.co_name
    code=linecache.getline(filename, line)
    if "self" in frame.f_locals:
        classname= frame.f_locals["self"].__class__.__qualname__
    else:
        classname="NN"
    #print( "global", event, filename, line, classname, name, code)
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
    
    exec(cmd )

    myfile.write("}\n")
    myfile.close()

main()
